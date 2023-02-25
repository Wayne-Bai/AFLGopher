import pandas as pd
import os


data = pd.read_csv("/home/eval5/Documents/aflgo/FinalCode/CFG_phase/if_cluster.csv")

data['count'] = ''
data['taken'] = ''

row_num = data.shape[0]

dynamic_list = []

#with open(os.environ.get('TMP_DIR') +'/'+'ifTotal', 'r') as f:
with open('/home/eval5/Documents/aflgo/FinalCode/CFG_phase/ifTotal', 'r') as f:
    for line in f.readlines():
        prob_data = line.split()
        dynamic_list.append(prob_data)
f.close()

for i in range(row_num):
    for j in dynamic_list:
        if data.iloc[i].at['file'] == j[1] and data.iloc[i].at['line'] == j[2]:
            data.loc[i, 'count'] = j[4]
            data.loc[i, 'taken'] = j[6]

data.to_csv('/home/eval5/Documents/aflgo/FinalCode/CFG_phase/if_update.csv')

