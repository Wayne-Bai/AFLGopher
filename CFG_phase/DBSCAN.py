import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from matplotlib import pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
import seaborn
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--category", default=None)

args = parser.parse_args()

file_name = args.category
# file_name = 'global'
# file_name = 'function'
# file_name = 'argument'
# file_name = 'if'

if file_name == 'global':
	data = pd.read_csv("global_input.csv")
	original_data = pd.read_csv('global.csv')
elif file_name == 'function':
	data = pd.read_csv("function_input.csv")
	original_data = pd.read_csv('function.csv')
elif file_name == 'argument':
	data = pd.read_csv("argument_input.csv")
	original_data = pd.read_csv('argument.csv')
elif file_name == 'if':
	data = pd.read_csv("if_input.csv")
	original_data = pd.read_csv("if_data.csv")
else:
	print("Please provide correct category")
	sys.exit(0)


# select emp
neighbors = NearestNeighbors(n_neighbors=3)
neighbors_fit = neighbors.fit(data)
distances, indices = neighbors_fit.kneighbors(data)
distances = np.sort(distances, axis=0)
distances = distances[:, 2]

## TODO: Generate graph
plt.plot(distances)
plt.show()


db = DBSCAN(eps=0.25, min_samples=3).fit(data) # global: 0.25, 6; function: 0.25, 3; argument: 0.15, 2

labels = db.labels_

# TODO: Select the best parameters
# temp_list = []
# for i in range(15, 30):
# 	for j in range(3,10):
# 		print('parameter: {}, {}'.format(i,j))
# 		db = DBSCAN(eps=i, min_samples=j).fit(data)	# if==25
#
# 		labels = db.labels_
#
# 		sample_cores = np.zeros_like(labels, dtype=bool)
#
# 		sample_cores[db.core_sample_indices_] = True
#
# 		# Calculating the number of clusters
# 		n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
# 		print(metrics.silhouette_score(data, labels))
# 		print(n_clusters)
#
# 		n_noise_ = list(labels).count(-1)
# 		temp_list.append(metrics.silhouette_score(data, labels))
# 		print("Estimated number of noise points: %d" % n_noise_)
#
# print("max_score: {}".format(max(temp_list)))

original_data['label'] = pd.DataFrame(labels)
# print(data.shape)

if file_name == 'global':
	original_data.to_csv('global_cluster.csv', index=False)
elif file_name == 'function':
	original_data.to_csv('function_cluster.csv', index=False)
elif file_name == 'argument':
	original_data.to_csv('argument_cluster.csv', index=False)
elif file_name == 'if':
	original_data.to_csv('if_cluster.csv', index=False)

# identifying the points which makes up our core points
sample_cores = np.zeros_like(labels,dtype=bool)

sample_cores[db.core_sample_indices_] = True

#Calculating the number of clusters
n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
print(metrics.silhouette_score(data,labels))
print("***Number of Clusters***: %d" % n_clusters)

n_noise_ = list(labels).count(-1)
print("Estimated number of noise points: %d" % n_noise_)

l = list(labels)
cl_labels = [0] * n_clusters

for i in range(len(l)):
	if l[i] != -1:
		cl_labels[l[i]] = cl_labels[l[i]] + 1

# Print the number of elements inside each clusters
# for i in range(len(cl_labels)):
# 	print(i,"  ",cl_labels[i])

## TSNE
# model = TSNE(n_components = 2, random_state = 0)
# tsne_data = model.fit_transform(data)
# tsne_data = np.vstack((tsne_data.T, labels)).T
# tsne_df = pd.DataFrame(data = tsne_data, columns =("Dim_1", "Dim_2", "label"))
#
# seaborn.FacetGrid(tsne_df, hue="label", size=6).map(plt.scatter, 'Dim_1', 'Dim_2').add_legend()
#
# plt.show()