import numpy as np
import pandas as pd
import csv
from sklearn.metrics.pairwise import cosine_similarity, paired_distances


data = pd.read_csv("if_input.csv")

data_row, data_col = data.shape

data = np.array(data)

# a = data[0].reshape(1,9)

# print(data[0])

# def maxk(arraylist,k):
#
#     max_list=[]
#     max_list_id=[x for x in range(0,k)]
#     m=[max_list,max_list_id]
#
#     for i in max_list_id:
#         max_list.append(arraylist[i])
#
#     for i in range(k,len(arraylist)):
#         if arraylist[i]>min(max_list):
#             mm=max_list.index(min(max_list))
#             del m[0][mm]
#             del m[1][mm]
#             m[0].append(arraylist[i])
#             m[1].append(i)
#
#     return max_list, max_list_id

# with open('if_cos.csv', 'a') as w:
#
#     writer = csv.writer(w)
#
#     writer.writerow(["if_ID", "max_cos_similarity", "max_similarity_corresponding_ID"])
#
#     for i in range(data_row):
#
#         max_similarity_list = []
#
#         temp = []
#         temp.append(i)
#
#
#         for j in range(data_row):
#
#             simi = cosine_similarity(data[i].reshape(1,2730), data[j].reshape(1,2730))
#             max_similarity_list.append(simi.tolist()[0][0])
#
#             # print('cosine similarity:', simi)
#
#             # dist = paired_distances(data[i].reshape(-1,1), data[j].reshape(-1,1), metric='cosine')
#             # print('cosine distance:', dist)
#
#         max_list, index_list = maxk(max_similarity_list, 6)
#         print(max_list)
#         print(index_list)
#
#         temp.append(max_list)
#         temp.append(index_list)
#         writer.writerow(temp)

with open('if_cos_pair.csv', 'a') as w:

    writer = csv.writer(w)

    writer.writerow(["if_ID_1", "if_ID_2", "similarity"])

    for i in range(data_row):

        for j in range(i, data_row):

            temp = []
            temp.append(i)

            simi = cosine_similarity(data[i].reshape(1,2730), data[j].reshape(1,2730))
            temp.append(j)
            temp.append(simi[0].tolist())
            print(temp)


            writer.writerow(temp)


