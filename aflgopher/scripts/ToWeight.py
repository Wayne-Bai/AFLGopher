#!/usr/bin/env python
# coding: utf-8


import os


f = open(os.environ.get('TMP_DIR')+"/if_distance")
lines = f.readlines()
f.close
f = open(os.environ.get('TMP_DIR')+"/ifLookUp")
allIf = f.readlines()
f.close
if os.path.exists(os.environ.get('TMP_DIR')+"/weight"):
        os.remove(os.environ.get('TMP_DIR')+"/weight")
f = open(os.environ.get('TMP_DIR')+'/weight', 'a')




index=0

distance_dic = {}

for record in allIf:

	res=record.strip().split()
	file_name= res[1]
	file_line= res[2]
	k = file_name + ':' + file_line
	v = [res[4], res[6]]
	distance_dic[k] = v
print(len(distance_dic.keys()))

for line in lines:
	match=line.split()
	file_if=match[0]
	line_if=match[1].rstrip('+')
	key = file_if + ':' + line_if
	print(key)
	weight=match[2]
	weight_false=match[3]
	if (key in distance_dic.keys()):
		print(file_if, distance_dic[key][0], distance_dic[key][1], weight, weight_false, file=f)
		
		index+=1
		print(index)

f.close


