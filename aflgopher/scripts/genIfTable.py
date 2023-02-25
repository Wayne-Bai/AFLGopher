#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import re


# In[2]:


f = open(os.environ.get('TMP_DIR')+"/SortedBBnames.txt")
BBnames = f.readlines()
f = open(os.environ.get('TMP_DIR')+"/if_source_position.txt")
conStates = f.readlines()


# In[3]:


BBnames_re = r'([0-9a-zA-Z_]+.[a-z]+):([0-9]+)'
conStat_re = r'([0-9a-zA-Z_\/.-]+.[a-z]+)\s+([0-9]+)'


# In[4]:

if os.path.exists(os.environ.get('TMP_DIR')+'/ifLookUp') :
	os.remove(os.environ.get('TMP_DIR')+'/ifLookUp') 
for index_if, record_if in enumerate(conStates):
    matchcon = re.search(conStat_re, record_if, re.M|re.I)
    if (matchcon==None):
        continue
    path_if, file_if = os.path.split(matchcon.group(1))
    line_if=int(matchcon.group(2))
    for index_BB, record_BB in enumerate(BBnames):
        match = re.search(BBnames_re, record_BB, re.M|re.I)
        if (match==None):
            continue
        file_BB=match.group(1)
        line_BB=int(match.group(2))
        if (file_if==file_BB)and(line_if>=line_BB):
            if (index_BB+2> len(BBnames)):
                continue;
            match = re.search(BBnames_re, BBnames[index_BB+1], re.M|re.I)
            file_next=match.group(1)
            line_next=int(match.group(2))
            if (file_BB==file_next):
                if (line_if<line_next):
                    with open(os.environ.get('TMP_DIR')+'/ifLookUp', 'a') as f:
                        print(path_if,file_if,line_if,"[BB]",line_BB,"[next]",line_next, file=f)
                        break


# In[ ]:




