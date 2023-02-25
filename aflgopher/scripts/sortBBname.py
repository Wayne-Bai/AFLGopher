#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import re


# In[2]:


f = open(os.environ.get('TMP_DIR')+"/BBnames.txt")
BBnames = f.readlines()


# In[3]:


BBnames_re = r'([0-9a-zA-Z_]+.[a-z]+):([0-9]+)'


# In[4]:


current=""
queu=[]
for index, record in enumerate(BBnames):
    matchObj = re.search(BBnames_re, record, re.M|re.I)
    if (matchObj==None):
        continue
    file=matchObj.group(1)
    line=int(matchObj.group(2))
    if (current==file):
        continue
    current=file
    queu=[]
    for index_sort,record_sort in enumerate(BBnames):
        matchObj = re.search(BBnames_re, record_sort, re.M|re.I)
        if (matchObj==None):
            continue
        file_sort=matchObj.group(1)
        line_sort=int(matchObj.group(2))
        if (file_sort==current):
            queu.append(line_sort)
        
    queu.sort()    
    for item in queu:
        #print(current+":"+str(item))
        with open(os.environ.get('TMP_DIR')+'/SortedBBnames.txt', 'a') as f:
            print(current+":"+str(item), file=f)


# In[ ]:




