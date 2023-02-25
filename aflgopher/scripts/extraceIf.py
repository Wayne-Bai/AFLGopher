#!/usr/bin/env python
# coding: utf-8

# In[5]:


import os
import re


# In[6]:


f = open(os.environ.get('TMP_DIR')+"/SortedBBnames.txt")
BBnames = f.readlines()
f = open(os.environ.get('TMP_DIR')+"/ifLookUp")
allIf = f.readlines()

if_count_dic = {}
if_taken_dic = {}
if_pair_dic = {}

for line in allIf:
    line_list = line.strip().split()
    if_p = line_list[1] + ':' + line_list[4]
    if_n = line_list[1] + ':' + line_list[6]
    if_count_dic[if_p] = 0
    if_taken_dic[if_n] = 0
    if_pair_dic[if_p] = if_n
    

    

# count the apperance
def countIf(dir):
    print("count if: "+dir)
    f = open(dir+"/elimData")
    trace = f.readlines()
    if os.path.exists(dir+"/ifCount"):
        os.remove(dir+"/ifCount") 
    
    for line in trace:
    	line_list = line.strip().split()
    	try:
    	    if_count_dic[line_list[-1]] += 1
    	except:
    	    try:
    	    	if_taken_dic[line_list[-1]] += 1
    	    except:
    	        pass
    

# In[7]:


trace_re = r'\[BB\]: ([0-9a-zA-Z_]+.[a-z]+):([0-9]+)'
BBnames_re = r'([0-9a-zA-Z_]+.[a-z]+):([0-9]+)'
conStat_re = r'[0-9]+\s([0-9a-zA-Z_\/.-]+.[a-z]+)\s([0-9]+)'
allIf_re = r'[0-9a-zA-Z_\/.-]+\s([0-9a-zA-Z_\/.-]+.[a-z]+)\s+([0-9]+)\s+\[BB]\s([0-9]+)\s+\[next]\s([0-9]+)'


# In[8]:


# sorted trace by filename, so that we can trace the execution in single file.
def preprocess(dir):
    print("preprocessing: "+dir)
    f = open(dir+"/trace")
    trace = f.readlines()
    if os.path.exists(dir+"/sortedData"):
        os.remove(dir+"/sortedData") 
    fileList=[]
    for index, record in enumerate(trace):
        match=record.split(':')
        if(len(match)<2):
            continue
        file=match[0]
        line=int(match[1])
        if file not in fileList:
            fileList.append(file)
    #print(fileList)
    for current in fileList:
        printList=[]
        for index, record in enumerate(trace):
            match=record.split(':')
            if(len(match)<2):
                continue
            file=match[0]
            line=int(match[1])
            if (file==current):
                printList.append(line)
        with open(dir+"/sortedData", 'a') as f:
            for item in printList:
                print("[BB]: "+current+":"+str(item),file=f)



# calculate possibility
def calPoss(dir):
	if os.path.exists(os.environ.get('TMP_DIR')+"/ifTotal"):
        	os.remove(os.environ.get('TMP_DIR')+"/ifTotal") 
	with open(os.environ.get('TMP_DIR')+"/ifTotal", 'a') as f:
		for k,v in if_count_dic.items():
			if v != 0:
				if_count = v
				if_taken = if_taken_dic[if_pair_dic[k]]
				takenPoss=round(if_taken/if_count,4)
				unPoss=1-takenPoss
				if takenPoss > 0:
				    print('libxml_ef709ce2', k,"[count]",if_count,"[taken]",if_taken, "[takePoss]", takenPoss, "[unPoss]", unPoss, file=f)
    	


# In[13]:


def ElimDoubleExec(dir):
    print("eliminate double execution: "+dir)
    f = open(dir+"/sortedData")
    trace = f.readlines()
    if os.path.exists(dir+"/elimData"):
        os.remove(dir+"/elimData") 
    for index, record in enumerate(trace):
        match=record.split(':')
        if(len(match)<2):
            continue
        tmp=match[1].split(' ')
        file=tmp[1]
        line=int(match[2])
        if (index+1>=len(trace)):
            with open(dir+"/elimData", 'a') as f:
                print("[BB]: "+file+":"+str(line), file=f)
            break
        match2=trace[index+1].split(':')
        if(len(match2)<2):
            continue
        tmp2=match2[1].split(' ')
        file_next=tmp2[1]
        if (file_next==file):
            line_next=int(match2[2])
            if (line_next==line):
                #print(file,line,file_next,line_next)
                continue
        with open(dir+"/elimData", 'a') as f:
            print("[BB]: "+file+":"+str(line), file=f)


# In[54]:


#run
parentDir=os.environ.get('IP_DIR')+"/BB"
for s in os.listdir(parentDir):
    preprocess(parentDir+"/"+s)
    ElimDoubleExec(parentDir+"/"+s)
    countIf(parentDir+"/"+s)
calPoss(parentDir)


