from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import numpy as np
import sys

data = pd.read_csv("if_input.csv")
if_data = pd.read_csv('if_symbol.csv')
# if_data = pd.read_csv('if_cluster_symbol.csv')

row = data.shape[0]

index_col = [x for x in range(row)]

data['index'] = index_col
data['count'] = 0
data['taken'] = 0

taken_dic = {}

with open('ifTotal', 'r') as f:
    for line in f.readlines():
        prob_data = line.strip().split()
        k = prob_data[1] + ':' + prob_data[2]
        v= [int(prob_data[4]), int(prob_data[6])]
        taken_dic[k] = v
f.close()
# print(taken_dic)
# sys.exit()

for i in range(data.shape[0]):
    position = if_data.loc[i, 'file'] + ':' + if_data.loc[i, 'line']
    if position in taken_dic.keys():
        data.loc[i,'count'] = taken_dic[position][0]
        data.loc[i, 'taken'] = taken_dic[position][1]


new_data = data.drop(columns=['index', 'count', 'taken'])

data_cosine=pd.DataFrame(cosine_similarity(new_data,dense_output=True))

# print(data_cosine.shape)

# cs = []
# plt.figure(figsize=(10,6))
# for i in range(1, 11):
#     kmeans = KMeans(n_clusters = i, init = 'k-means++', max_iter = 300, n_init = 10, random_state = 0)
#     kmeans.fit(data_cosine)
#     cs.append(kmeans.inertia_)
# plt.plot(range(1, 11), cs)
# plt.title('The Elbow Method')
# plt.xlabel('Number of clusters')
# plt.ylabel('CS')
# plt.show()


data_input = data_cosine
pca = PCA(2)
transform = pca.fit_transform(data_input)

# Initialize the class object
kmeans = KMeans(n_clusters=10)

# predict the labels of clusters.
label = kmeans.fit_predict(transform)

# Getting unique labels
u_labels = np.unique(label)

# print(display(label))
# print(display(u_labels))

cluster_data = {'Name':data['index'],'Cluster':label, 'Count': data['count'], 'Taken': data['taken']}
if_list = pd.DataFrame(cluster_data)
if_list['probability'] = 0

cluster_center = kmeans.cluster_centers_

cluster_possibility = []

for i in range(10):

    temp_data = if_list[if_list["Cluster"] == i]
    count_sum = temp_data['Count'].sum()
    taken_sum = temp_data['Taken'].sum()


    if count_sum != 0:
        prob = taken_sum/count_sum
        cluster_possibility.append(prob)

    else:
        cluster_possibility.append('no value')

print(cluster_possibility)

with open('group_probability', 'a') as w:
    for i in range(len(cluster_possibility)):

        temp_min_distance = 10000

        if cluster_possibility[i] == 'no value' or cluster_possibility[i] == 1:
            for j in range(len(cluster_center)):
                if j != i and cluster_possibility[j] != 'no value' and cluster_possibility[j] != 1:
                    dist = np.linalg.norm(cluster_center[i] - cluster_center[j])
                    if dist < temp_min_distance:
                        cluster_possibility[i] = cluster_possibility[j]
                        temp_min_distance = dist
        w.write(str(i))
        w.write('\t')
        w.write(str(cluster_possibility[i]))
        w.write('\n')
w.close()

print('cluster possibility: {}'.format(cluster_possibility))

for i in range(if_list.shape[0]):
    # if_list[if_list["Cluster"] == i]['probability'] = cluster_possibility[i]
    if_list.loc[i, 'probability'] = cluster_possibility[if_list.loc[i,'Cluster']]

# if_list.to_csv('if_probability.csv')
if_data['probability'] = if_list['probability']

with open('if_distance', 'a') as w:
    for i in range(if_data.shape[0]):
        w.write(if_data.loc[i, 'file'])
        w.write('\t')
        w.write(if_data.loc[i, 'line'])
        w.write('\t')
        if if_data.loc[i,'symbol'] == '==' or  if_data.loc[i,'symbol'] == '>' or if_data.loc[i,'symbol'] == '<':
            w.write(str(1 / if_data.loc[i, 'probability']))
            w.write('\t')
            w.write(str((1 / (1 - if_data.loc[i, 'probability']))))
            w.write('\n')
        else:
            w.write(str((1 / (1-if_data.loc[i, 'probability']))))
            w.write('\t')
            w.write(str(1 / if_data.loc[i, 'probability']))
            w.write('\n')

w.close()
# if_data['cluster'] = if_list['Cluster']
# if_data_new = if_data.drop(columns=['source 1', 'source 2', 'source 3'])
# if_data_new.to_csv('if_with_cluster.csv')



# plt.figure(figsize=(10,6))
# for i in u_labels:
#     plt.scatter(transform[label == i , 0] , transform[label == i , 1] , label = i)
# plt.scatter(kmeans.cluster_centers_[:,0],kmeans.cluster_centers_[:,1],color='purple',marker='+',label='centroid')
# plt.legend()
# plt.savefig('cluster.png')
# plt.show()