import pandas as pd
import numpy as np

# data = pd.read_csv("if_cluster.csv")
data = pd.read_csv("if_dynamic_taken.csv")
pair = pd.read_csv("if_cos_pair.csv")

# data['count'] = ''
# data['taken'] = ''
#
# row_num = data.shape[0]
#
# dynamic_list = []
#
# with open('ifTotal', 'r') as f:
#     for line in f.readlines():
#         prob_data = line.split()
#         dynamic_list.append(prob_data)
# f.close()
#
# for i in range(row_num):
#     for j in dynamic_list:
#         if data.iloc[i].at['file'] == j[1] and data.iloc[i].at['line'] == j[2]:
#             data.loc[i, 'count'] = j[4]
#             data.loc[i, 'taken'] = j[6]
#
# data.to_csv('if_dynamic_taken.csv')

# data_filter = data[(data['count'].notna()) & (data['count'] != '')]

data_row = data.shape[0]

cluster = []
used_ID = []

for i in range(data_row):
	if i not in used_ID:

		temp = []
		temp.append(i)
		used_ID.append(i)

		for j in range(i, data_row):

			row_ID = pair.loc[(pair['if_ID_1'] == i) & (pair['if_ID_2'] == j)]
			similarity = row_ID['similarity'].values
			similarity_value = float(similarity[0][1: -2])

			if similarity_value >= 0.72:
				if j not in temp:
					temp.append(j)
				if j not in used_ID:
					used_ID.append(j)

		print(i)
		print(temp)
		cluster.append(temp)

print('number of cluster: {}'.format(len(cluster)))

