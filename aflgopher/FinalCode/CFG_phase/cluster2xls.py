from xlrd import open_workbook
from xlutils.copy import copy
import pandas as pd

workbook = open_workbook('data.xls')
original_data = workbook.sheet_by_index(0)
excel = copy(workbook)
data = excel.get_sheet(0)
rows = workbook.sheets()[0].nrows

global_cluster = pd.read_csv("global_cluster.csv")
function_cluster = pd.read_csv("function_cluster.csv")
argument_cluster = pd.read_csv("argument_cluster.csv")

# print(global_cluster.at[0,'combination'])
# print((type(global_cluster.at[0,'combination'])))
#
# global_cluster['combination'].astype(str)
# print(global_cluster['combination'].dtype)

for i in range(1, rows):

	# Global
	if original_data.cell_value(i, 3) == 'global':

		index_list = global_cluster[global_cluster.combination == original_data.cell_value(i, 6)].index.tolist()
		try:
			label = global_cluster.at[index_list[0], 'label']
			data.write(i, 7, 'global_'+ str(label).split('.')[0])
		except:
			print(original_data.cell_value(i, 6))
	if original_data.cell_value(i, 8) == 'global':

		index_list = global_cluster[global_cluster.combination == original_data.cell_value(i, 11)].index.tolist()
		try:
			label = global_cluster.at[index_list[0], 'label']
			data.write(i, 12, 'global_'+ str(label).split('.')[0])
		except:
			print(original_data.cell_value(i, 11))

	if original_data.cell_value(i, 13) == 'global':

		index_list = global_cluster[global_cluster.combination == original_data.cell_value(i, 16)].index.tolist()
		try:
			label = global_cluster.at[index_list[0], 'label']
			data.write(i, 17, 'global_'+ str(label).split('.')[0])
		except:
			print(original_data.cell_value(i, 16))

	# Function
	if original_data.cell_value(i, 3) == 'function':

		index_list = function_cluster[function_cluster.combination == original_data.cell_value(i, 6)].index.tolist()
		try:
			label = function_cluster.at[index_list[0], 'label']
			data.write(i, 7, 'function_'+ str(label).split('.')[0])
		except:
			print(original_data.cell_value(i, 6))
	if original_data.cell_value(i, 8) == 'function':

		index_list = function_cluster[function_cluster.combination == original_data.cell_value(i, 11)].index.tolist()
		try:
			label = function_cluster.at[index_list[0], 'label']
			data.write(i, 12, 'function_'+ str(label).split('.')[0])
		except:
			print(original_data.cell_value(i, 11))

	if original_data.cell_value(i, 13) == 'function':

		index_list = function_cluster[function_cluster.combination == original_data.cell_value(i, 16)].index.tolist()
		try:
			label = function_cluster.at[index_list[0], 'label']
			data.write(i, 17, 'function_'+ str(label).split('.')[0])
		except:
			print(original_data.cell_value(i, 16))


	# Argument
	if original_data.cell_value(i, 3) == 'argument':

		index_list = argument_cluster[argument_cluster.combination == original_data.cell_value(i, 6)].index.tolist()
		try:
			label = argument_cluster.at[index_list[0], 'label']
			data.write(i, 7, 'argument_'+ str(label).split('.')[0])
		except:
			print(original_data.cell_value(i, 6))
	if original_data.cell_value(i, 8) == 'argument':

		index_list = argument_cluster[argument_cluster.combination == original_data.cell_value(i, 11)].index.tolist()
		try:
			label = argument_cluster.at[index_list[0], 'label']
			data.write(i, 12, 'argument_'+ str(label).split('.')[0])
		except:
			print(original_data.cell_value(i, 11))

	if original_data.cell_value(i, 13) == 'argument':

		index_list = argument_cluster[argument_cluster.combination == original_data.cell_value(i, 16)].index.tolist()
		try:
			label = argument_cluster.at[index_list[0], 'label']
			data.write(i, 17, 'argument_'+ str(label).split('.')[0])
		except:
			print(original_data.cell_value(i, 16))

excel.save("data.xls")


# 	exit()