/*
   american fuzzy lop - LLVM-mode instrumentation pass
   ---------------------------------------------------

   Written by Laszlo Szekeres <lszekeres@google.com> and
              Michal Zalewski <lcamtuf@google.com>

   LLVM integration design comes from Laszlo Szekeres. C bits copied-and-pasted
   from afl-as.c are Michal's fault.

   Copyright 2015, 2016 Google Inc. All rights reserved.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at:

     http://www.apache.org/licenses/LICENSE-2.0

   This library is plugged into LLVM when invoking clang through afl-clang-fast.
   It tells the compiler to add code roughly equivalent to the bits discussed
   in ../afl-as.h.

 */

#define AFL_LLVM_PASS

#include "../config.h"
#include "../debug.h"

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <list>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#include "llvm/ADT/Statistic.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/LegacyPassManager.h"
#include "llvm/IR/Module.h"
#include "llvm/Support/Debug.h"
#include "llvm/Transforms/IPO/PassManagerBuilder.h"
#include "llvm/Support/CommandLine.h"
#include "llvm/Support/FileSystem.h"
#include "llvm/Support/raw_ostream.h"
#include "llvm/Analysis/CFGPrinter.h"

#if defined(LLVM34)
#include "llvm/DebugInfo.h"
#else
#include "llvm/IR/DebugInfo.h"
#endif

#if defined(LLVM34) || defined(LLVM35) || defined(LLVM36)
#define LLVM_OLD_DEBUG_API
#endif

using namespace llvm;

cl::opt<std::string> DistanceFile(
    "distance",
    cl::desc("Distance file containing the distance of each basic block to the provided targets."),
    cl::value_desc("filename")
);

cl::opt<std::string> TargetsFile(
    "targets",
    cl::desc("Input file containing the target lines of code."),
    cl::value_desc("targets"));

cl::opt<std::string> OutDirectory(
    "outdir",
    cl::desc("Output directory where Ftargets.txt, Fnames.txt, and BBnames.txt are generated."),
    cl::value_desc("outdir"));

namespace llvm {

template<>
struct DOTGraphTraits<Function*> : public DefaultDOTGraphTraits {
  DOTGraphTraits(bool isSimple=true) : DefaultDOTGraphTraits(isSimple) {}

  static std::string getGraphName(Function *F) {
    return "CFG for '" + F->getName().str() + "' function";
  }

  std::string getNodeLabel(BasicBlock *Node, Function *Graph) {
    if (!Node->getName().empty()) {
      return Node->getName().str();
    }

    std::string Str;
    raw_string_ostream OS(Str);

    Node->printAsOperand(OS, false);
    return OS.str();
  }
};

} // namespace llvm

namespace {

  class AFLCoverage : public ModulePass {

    public:

      static char ID;
      AFLCoverage() : ModulePass(ID) { }

      bool runOnModule(Module &M) override;

      // StringRef getPassName() const override {
      //  return "American Fuzzy Lop Instrumentation";
      // }

  };

}

char AFLCoverage::ID = 0;

static void getDebugLoc(const Instruction *I, std::string &Filename,
                        unsigned &Line) {
#ifdef LLVM_OLD_DEBUG_API
  DebugLoc Loc = I->getDebugLoc();
  if (!Loc.isUnknown()) {
    DILocation cDILoc(Loc.getAsMDNode(M.getContext()));
    DILocation oDILoc = cDILoc.getOrigLocation();

    Line = oDILoc.getLineNumber();
    Filename = oDILoc.getFilename().str();

    if (filename.empty()) {
      Line = cDILoc.getLineNumber();
      Filename = cDILoc.getFilename().str();
    }
  }
#else
  if (DILocation *Loc = I->getDebugLoc()) {
    Line = Loc->getLine();
    Filename = Loc->getFilename().str();

    if (Filename.empty()) {
      DILocation *oDILoc = Loc->getInlinedAt();
      if (oDILoc) {
        Line = oDILoc->getLine();
        Filename = oDILoc->getFilename().str();
      }
    }
  }
#endif /* LLVM_OLD_DEBUG_API */
}

static bool isBlacklisted(const Function *F) {
  static const SmallVector<std::string, 8> Blacklist = {
    "asan.",
    "llvm.",
    "sancov.",
    "__ubsan_handle_",
    "free",
    "malloc",
    "calloc",
    "realloc"
  };

  for (auto const &BlacklistFunc : Blacklist) {
    if (F->getName().startswith(BlacklistFunc)) {
      return true;
    }
  }

  return false;
}

bool AFLCoverage::runOnModule(Module &M) {

  bool is_aflgo = false;
  bool is_aflgo_preprocessing = false;
  int base_index = 0;
  int base_index_cg = 0;
  
  std::ifstream table;
  table.open(OutDirectory + "/BBtableIndex.txt",std::ios::in);
  
  if (table.fail()){
  	base_index = 0;
  }else{
  	if(!(table>> base_index))
  		base_index=0;
  }
  
  std::ifstream table_cg;
  table_cg.open(OutDirectory + "/CGtableIndex.txt",std::ios::in);
  
  if (table_cg.fail()){
  	base_index_cg = 0;
  }else{
  	if(!(table_cg>> base_index_cg))
  		base_index_cg=0;
  }
  

  if (!TargetsFile.empty() && !DistanceFile.empty()) {
    FATAL("Cannot specify both '-targets' and '-distance'!");
    return false;
  }

  std::list<std::string> targets;
  std::map<std::string, int> bb_to_dis;
  std::vector<std::string> basic_blocks;

  if (!TargetsFile.empty()) {

    if (OutDirectory.empty()) {
      FATAL("Provide output directory '-outdir <directory>'");
      return false;
    }

    std::ifstream targetsfile(TargetsFile);
    std::string line;
    while (std::getline(targetsfile, line))
      targets.push_back(line);
    targetsfile.close();

    is_aflgo_preprocessing = true;

  } else if (!DistanceFile.empty()) {

    std::ifstream cf(DistanceFile);
    if (cf.is_open()) {

      std::string line;
      while (getline(cf, line)) {

        std::size_t pos = line.find(",");
        std::string bb_name = line.substr(0, pos);
        int bb_dis = (int) (100.0 * atof(line.substr(pos + 1, line.length()).c_str()));

        bb_to_dis.emplace(bb_name, bb_dis);
        basic_blocks.push_back(bb_name);

      }
      cf.close();

      is_aflgo = true;

    } else {
      FATAL("Unable to find %s.", DistanceFile.c_str());
      return false;
    }

  }

  /* Show a banner */

  char be_quiet = 0;

  if (isatty(2) && !getenv("AFL_QUIET")) {

    if (is_aflgo || is_aflgo_preprocessing)
      SAYF(cCYA "aflgo-llvm-pass (yeah!) " cBRI VERSION cRST " (%s mode)\n",
           (is_aflgo_preprocessing ? "preprocessing" : "distance instrumentation"));
    else
      SAYF(cCYA "afl-llvm-pass " cBRI VERSION cRST " by <lszekeres@google.com>\n");


  } else be_quiet = 1;

  /* Decide instrumentation ratio */

  char* inst_ratio_str = getenv("AFL_INST_RATIO");
  unsigned int inst_ratio = 100;

  if (inst_ratio_str) {

    if (sscanf(inst_ratio_str, "%u", &inst_ratio) != 1 || !inst_ratio ||
        inst_ratio > 100)
      FATAL("Bad value of AFL_INST_RATIO (must be between 1 and 100)");

  }

  /* Default: Not selective */
  char* is_selective_str = getenv("AFLGO_SELECTIVE");
  unsigned int is_selective = 0;

  if (is_selective_str && sscanf(is_selective_str, "%u", &is_selective) != 1)
    FATAL("Bad value of AFLGO_SELECTIVE (must be 0 or 1)");

  char* dinst_ratio_str = getenv("AFLGO_INST_RATIO");
  unsigned int dinst_ratio = 100;

  if (dinst_ratio_str) {

    if (sscanf(dinst_ratio_str, "%u", &dinst_ratio) != 1 || !dinst_ratio ||
        dinst_ratio > 100)
      FATAL("Bad value of AFLGO_INST_RATIO (must be between 1 and 100)");

  }

  /* Instrument all the things! */

  int inst_blocks = 0;
  int index_BB=base_index;
  int index_CG=base_index_cg;
  

    // instrument start


    LLVMContext &C = M.getContext();
    IntegerType *Int8Ty  = IntegerType::getInt8Ty(C);
    IntegerType *Int32Ty = IntegerType::getInt32Ty(C);
    IntegerType *Int64Ty = IntegerType::getInt64Ty(C);

#ifdef __x86_64__
    IntegerType *LargestType = Int64Ty;
    ConstantInt *MapCntLoc = ConstantInt::get(LargestType, MAP_SIZE + 8);
    ConstantInt *MapTargloc = ConstantInt::get(LargestType, MAP_SIZE + 16);
#else
    IntegerType *LargestType = Int32Ty;
    ConstantInt *MapCntLoc = ConstantInt::get(LargestType, MAP_SIZE + 4);
    ConstantInt *MapTargloc = ConstantInt::get(LargestType, MAP_SIZE + 8);
#endif
    ConstantInt *MapDistLoc = ConstantInt::get(LargestType, MAP_SIZE);
    ConstantInt *One = ConstantInt::get(LargestType, 1);

    /* Get globals for the SHM region and the previous location. Note that
       __afl_prev_loc is thread-local. */

    GlobalVariable *AFLMapPtr =
        new GlobalVariable(M, PointerType::get(Int8Ty, 0), false,
                           GlobalValue::ExternalLinkage, 0, "__afl_area_ptr");

    GlobalVariable *AFLPrevLoc = new GlobalVariable(
        M, Int32Ty, false, GlobalValue::ExternalLinkage, 0, "__afl_prev_loc",
        0, GlobalVariable::GeneralDynamicTLSModel, 0, false);





    std::ofstream bbnames(OutDirectory + "/BBnames.txt", std::ofstream::out | std::ofstream::app);
    std::ofstream bbcalls(OutDirectory + "/BBcalls.txt", std::ofstream::out | std::ofstream::app);
    std::ofstream fnames(OutDirectory + "/Fnames.txt", std::ofstream::out | std::ofstream::app);
    std::ofstream cnames(OutDirectory + "/Cnames.txt", std::ofstream::out | std::ofstream::app);
    std::ofstream ftargets(OutDirectory + "/Ftargets.txt", std::ofstream::out | std::ofstream::app);
    std::ofstream bbtable(OutDirectory + "/BBtable.txt", std::ofstream::out | std::ofstream::app);
    std::ofstream bbtableIndex(OutDirectory + "/BBtableIndex.txt", std::ofstream::out );
    std::ofstream cgtable(OutDirectory + "/CGtable.txt", std::ofstream::out | std::ofstream::app);
    std::ofstream cgtableIndex(OutDirectory + "/CGtableIndex.txt", std::ofstream::out );
    std::ofstream IfCallGraph(OutDirectory + "/If_Call.txt", std::ofstream::out | std::ofstream::app);

    /* Create dot-files directory */
    std::string dotfiles(OutDirectory + "/dot-files");
    /*if (sys::fs::create_directory(dotfiles)) {
      FATAL("Could not create directory %s.", dotfiles.c_str());
    }*/

    for (auto &F : M) {

      bool has_BBs = false;
      std::string funcName = F.getName().str();

      /* Black list of function names */
      if (isBlacklisted(&F)) {
        continue;
      }
      
      /*edit*/
      unsigned start_line;
      bool have_start_line=false;
      bool f_trace= true;
      
      bool is_target = false;
      bool insert_count = false;
      
      for (auto &BB : F) {

        std::string bb_name("");
        std::string filename;
        unsigned line;

	// CG level trace
	//insert to start of the function
        
        Type *Args0[] = {
		      Type::getInt8PtrTy(M.getContext()) //uint8_t* bb_name
		  };
	FunctionType *FTy0 = FunctionType::get(Type::getVoidTy(M.getContext()), Args0, false);
		  
	auto Callee0 = M.getOrInsertFunction("llvm_profiling_call", FTy0);
        
        if (f_trace){
          	
          	  index_CG++;
		  std::string f_name=M.getSourceFileName()+" "+F.getName().str();

        	  IRBuilder<> Builder0(&(*(BB.getFirstNonPHIOrDbgOrLifetime())));

		  Value *cgVal = Builder0.CreateGlobalStringPtr("cg "+std::to_string(index_CG));
		  cgtable << index_CG<<" "<< f_name <<"\n";
		  
		  Builder0.CreateCall(Callee0, {cgVal});
		  f_trace=false;
        }

        for (auto &I : BB) {
	  
          getDebugLoc(&I, filename, line);
          
          
          
          // get if-call graph
          if (isa<CallInst>(I)){
          	auto *CI=dyn_cast<CallInst>(&I);
          	Function *fun = CI->getCalledFunction();
 		//directed call
 		if (fun) {
		  	std::string callee;
		  	StringRef callFunction=fun->getName();
		  	callee= callFunction.str();
		  	for (auto it = pred_begin(&BB), et = pred_end(&BB); it != et; ++it){
	  			BasicBlock* predecessor = *it;
	  			for (auto &inst : *predecessor){
	  				if (isa<BranchInst>(&inst)){
	  					std::string brachFile;
	  					unsigned branchLine;
	  					getDebugLoc(&inst, brachFile, branchLine);
	  					IfCallGraph <<funcName<< " "<< filename<<" "<< branchLine<< " -> " << callee <<" "<< line<< "\n";
	  					
	  				}
	  			
	  			}
			}
        	
        	}
          }
          
          
          
          
          /* Don't worry about external libs */
          static const std::string Xlibs("/usr/");
          if (filename.empty() || line == 0 || !filename.compare(0, Xlibs.size(), Xlibs))
            continue;

          if (have_start_line==false){
          	start_line=line;
          	have_start_line=true;
          }

          if (bb_name.empty()) {

            std::size_t found = filename.find_last_of("/\\");
            if (found != std::string::npos)
              filename = filename.substr(found + 1);

            bb_name = filename + ":" + std::to_string(line);
          }

          if (!is_target) {
              for (auto &target : targets) {
                std::size_t found = target.find_last_of("/\\");
                if (found != std::string::npos)
                  target = target.substr(found + 1);

                std::size_t pos = target.find_last_of(":");
                std::string target_file = target.substr(0, pos);
                unsigned int target_line = atoi(target.substr(pos + 1).c_str());

                if (!target_file.compare(filename) && target_line == line){
                	is_target = true;
                	if (target.compare(targets.back()))
                		insert_count=true;
                }

              }
            }

            if (auto *c = dyn_cast<CallInst>(&I)) {

              std::size_t found = filename.find_last_of("/\\");
              if (found != std::string::npos)
                filename = filename.substr(found + 1);

              if (auto *CalledF = c->getCalledFunction()) {
                if (!isBlacklisted(CalledF))
                  bbcalls << bb_name << "," << CalledF->getName().str() << "\n";
              }
            }
        }

        if (!bb_name.empty()) {

          BB.setName(bb_name + ":");
          if (!BB.hasName()) {
            std::string newname = bb_name + ":";
            Twine t(newname);
            SmallString<256> NameData;
            StringRef NameRef = t.toStringRef(NameData);
            MallocAllocator Allocator;
            BB.setValueName(ValueName::Create(NameRef, Allocator));
          }

          bbnames << BB.getName().str() << "\n";
          has_BBs = true;

          auto *TI = BB.getTerminator();
          IRBuilder<> Builder(TI);


	  // BB level trace
	  index_BB++;
          Value *bbnameVal = Builder.CreateGlobalStringPtr("BB "+std::to_string(index_BB));
          bbtable<<index_BB<<" "<< bb_name <<"\n";
      
          
          Type *Args[] = {
              Type::getInt8PtrTy(M.getContext()) //uint8_t* bb_name
          };
          FunctionType *FTy = FunctionType::get(Type::getVoidTy(M.getContext()), Args, false);
          //Constant *instrumented = M.getOrInsertFunction("llvm_profiling_call", FTy);
          
          auto Callee = M.getOrInsertFunction("llvm_profiling_call", FTy);
          //auto instrumented = dyn_cast<Constant>(Callee.getCallee());
          
          Builder.CreateCall(Callee, {bbnameVal});

        }
        
        
        
        
      BasicBlock::iterator IP = BB.getFirstInsertionPt();
      IRBuilder<> IRB(&(*IP));

      if (AFL_R(100) >= inst_ratio) continue;

      /* Make up cur_loc */

      unsigned int cur_loc = AFL_R(MAP_SIZE);

      ConstantInt *CurLoc = ConstantInt::get(Int32Ty, cur_loc);

      /* Load prev_loc */

      LoadInst *PrevLoc = IRB.CreateLoad(AFLPrevLoc);
      PrevLoc->setMetadata(M.getMDKindID("nosanitize"), MDNode::get(C, None));
      Value *PrevLocCasted = IRB.CreateZExt(PrevLoc, IRB.getInt32Ty());

      /* Load SHM pointer */

      LoadInst *MapPtr = IRB.CreateLoad(AFLMapPtr);
      MapPtr->setMetadata(M.getMDKindID("nosanitize"), MDNode::get(C, None));
      Value *MapPtrIdx =
          IRB.CreateGEP(MapPtr, IRB.CreateXor(PrevLocCasted, CurLoc));

      /* Update bitmap */

      LoadInst *Counter = IRB.CreateLoad(MapPtrIdx);
      Counter->setMetadata(M.getMDKindID("nosanitize"), MDNode::get(C, None));
      Value *Incr = IRB.CreateAdd(Counter, ConstantInt::get(Int8Ty, 1));
      IRB.CreateStore(Incr, MapPtrIdx)
          ->setMetadata(M.getMDKindID("nosanitize"), MDNode::get(C, None));

      /* Set prev_loc to cur_loc >> 1 */

      StoreInst *Store =
          IRB.CreateStore(ConstantInt::get(Int32Ty, cur_loc >> 1), AFLPrevLoc);
      Store->setMetadata(M.getMDKindID("nosanitize"), MDNode::get(C, None));

	/* edited: indicator of reaching a target, each target got a uniq int number */
	/* Change value at shm[MAPSIZE + (8 or 16)] */

	if (insert_count) {
		  
		Value *MapTargPtr = IRB.CreateBitCast(
			IRB.CreateGEP(MapPtr, MapTargloc), LargestType->getPointerTo());
		LoadInst *MapTarg = IRB.CreateLoad(MapTargPtr);
		MapTarg->setMetadata(M.getMDKindID("nosanitize"), MDNode::get(C, None));

		Value *NewTarg = IRB.CreateAdd(MapTarg, One);
		IRB.CreateStore(NewTarg, MapTargPtr)
			->setMetadata(M.getMDKindID("nosanitize"), MDNode::get(C, None));
	}


      inst_blocks++;
        
        
        
        
        
        
      }

      if (has_BBs) {
        /* Print CFG */
        std::string cfgFileName = dotfiles + "/cfg." + funcName + ".dot";
        std::error_code EC;
        raw_fd_ostream cfgFile(cfgFileName, EC, sys::fs::F_None);
        if (!EC) {
          WriteGraph(cfgFile, &F, true);
        }

        if (is_target)
          ftargets << F.getName().str() << "\n";
        fnames << F.getName().str() << "\n";
        
        /* edited: get file name*/
        std::string file_name = M.getSourceFileName();
        cnames << file_name << " "<<F.getName().str() << " "<<  std::to_string(start_line) <<"\n";
      }
    }

  // instrument end


  /* Say something nice. */

  if (!is_aflgo_preprocessing && !be_quiet) {

    if (!inst_blocks) WARNF("No instrumentation targets found.");
    else OKF("Instrumented %u locations (%s mode, ratio %u%%, dist. ratio %u%%).",
             inst_blocks,
             getenv("AFL_HARDEN")
             ? "hardened"
             : ((getenv("AFL_USE_ASAN") || getenv("AFL_USE_MSAN"))
               ? "ASAN/MSAN" : "non-hardened"),
             inst_ratio, dinst_ratio);

  }

  bbtableIndex<<index_BB<<"\n";
  cgtableIndex<<index_CG<<"\n";

  return true;

}


static void registerAFLPass(const PassManagerBuilder &,
                            legacy::PassManagerBase &PM) {

  PM.add(new AFLCoverage());

}


static RegisterStandardPasses RegisterAFLPass(
    PassManagerBuilder::EP_OptimizerLast, registerAFLPass);

static RegisterStandardPasses RegisterAFLPass0(
    PassManagerBuilder::EP_EnabledOnOptLevel0, registerAFLPass);
