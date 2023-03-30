import re
CGpath= "./callgraph.dot"
edge_path= "./mlta_edges"
out_path= "newcallgraph.dot"
re_node=r'(Node[0-9a-zA-Z]+)\s\[shape=record,label="{([a-zA-Z]+)}"\]'


def find_node(func):
	fnode = open(CGpath,"r")
	items = fnode.readlines()
	for item in items:
		match = re.search(re_node, item, re.M|re.I)
		if (match==None):
			continue
		node_name = match.group(1)
		func_name = match.group(2)
		if (func==func_name):
			return node_name
	return None


f=open(edge_path,"r")
lines=f.readlines()

applist=[]


for line in lines:
	res = line.split()
	f_src=res[0]
	f_des=res[1]
	node_src = find_node(f_src)
	node_des = find_node(f_des)
	if node_src==None or node_des==None:
		continue
	newstring="	"+str(node_src)+" -> "+str(node_des)+"\n"
	applist.append(newstring)

fin = open(CGpath,"r")
new_line= fin.readlines()
fnode = open(out_path,"a")
for lista in applist:
	new_line.insert(len(new_line)-1, lista)
for listb in new_line:
	fnode.write(listb)
