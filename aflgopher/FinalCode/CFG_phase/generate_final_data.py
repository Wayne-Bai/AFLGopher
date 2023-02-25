from xlrd import open_workbook
from xlutils.copy import copy
import pandas as pd
import xlwt

workbook = open_workbook('data.xls')
original_data = workbook.sheet_by_index(0)
excel = copy(workbook)
data = excel.get_sheet(0)
rows = workbook.sheets()[0].nrows

if_cluster = pd.read_csv("whole_if_data.csv")

workbook1 = xlwt.Workbook(encoding='utf-8')
worksheet = workbook1.add_sheet('IF statement', cell_overwrite_ok=True)

# add HEAD
worksheet.write(0, 0, label='File Name')
worksheet.write(0, 1, label='Line')
worksheet.write(0, 2, label='Operator')
worksheet.write(0, 3, label='Left Value Cluster')
worksheet.write(0, 4, label='Right Value Cluster')
worksheet.write(0, 5, label='Additional Cluster')
worksheet.write(0, 6, label='IF Statement Category')
worksheet.write(0, 7, label='Similarity Score')
worksheet.write(0, 8, label='Similar IF Statement')
worksheet.write(0, 9, label='True Branch Similarity')
worksheet.write(0, 10, label='False Branch Similarity')

val = 1

for i in range(1, rows):

	if if_cluster[(if_cluster.file == original_data.cell_value(i, 0)) & (if_cluster.line ==
				  original_data.cell_value(i, 1))].index.tolist():

		index_list = if_cluster[(if_cluster.file == original_data.cell_value(i, 0)) & (if_cluster.line ==
				  original_data.cell_value(i, 1))].index.tolist()

	# TODO:
		file_name = if_cluster.at[index_list[0], 'file']
		line = if_cluster.at[index_list[0], 'line']
		operator_name = original_data.cell_value(i,2)
		left_value = if_cluster.at[index_list[0], 'source 1']
		right_value = if_cluster.at[index_list[0], 'source 2']
		additional_value = if_cluster.at[index_list[0], 'source 3']

		if operator_name == '==' or operator_name == '!=' or operator_name == '!':
			IF_category = 'Equal'
		elif operator_name == '>' or operator_name == '<=':
			IF_category = 'Larger'
		elif operator_name == '<' or operator_name == '>=':
			IF_category = 'Smaller'

		similarity_score = if_cluster.at[index_list[0], 'max_cos_similarity']
		similar_IF = if_cluster.at[index_list[0], 'max_similarity_corresponding_ID']

		worksheet.write(val, 0, file_name)
		worksheet.write(val, 1, line)
		worksheet.write(val, 2, operator_name)
		worksheet.write(val, 3, left_value)
		worksheet.write(val, 4, right_value)
		worksheet.write(val, 5, additional_value)
		worksheet.write(val, 6, IF_category)
		worksheet.write(val, 7, str(similarity_score))
		worksheet.write(val, 8, str(similar_IF))

		val += 1



workbook1.save('Final IF.xls')