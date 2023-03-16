import re
import os

re_line=r'\[([a-zA-Z]+)\]\s([a-zA-Z0-9\/.-]+)\s\+([0-9]+)\s([a-zA-Z0-9_+-]+)'
re_=r'Node[0-9a-zA-Z]+\s\[shape=record,label="{([a-zA-Z]+)}"\]'


f=open("mlta_res_path.txt","r")
lines=f.readlines()
for line in lines:
	line=line.strip("\n")
	file_path="./mjs-issues-78/"+line
	f_res=open(file_path,"r")
	res_lines=f_res.readlines()
	
	# get file content
	source_path=file_path[:-7]
	
	for res_line in res_lines:
		
		match =  re.search(re_line, res_line, re.M|re.I)
		if (match==None):
			continue
		Tag = match.group(1)
		if Tag!="CALLER":
			continue
		filename = match.group(2)
		line = match.group(3)
		f_src = match.group(4)
		
		result = os.popen('sed -n {}p {}'.format(line, source_path)).read().replace('\n', '')
		result, _ ,_ = result.partition('(')
		_, _, result = result.partition('=')
		
		for following_line in res_lines[res_lines.index(res_line)+1:] :
			match2 =  re.search(re_line, following_line, re.M|re.I)
			if (match2==None):
				continue
			Tag = match2.group(1)
			if Tag == "CALLER":
				break
			if Tag != "TARGET" :
				continue
			f_des=match2.group(4)
			print(f_src,f_des)
			with open("mlta_edges","a") as fout:
				print(f_src,f_des,result,file=fout)
	
