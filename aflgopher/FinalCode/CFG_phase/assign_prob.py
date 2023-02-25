from xlrd import open_workbook
from xlutils.copy import copy
import pandas as pd

workbook = open_workbook('Final IF.xls')
original_data = workbook.sheet_by_index(0)
excel = copy(workbook)
data = excel.get_sheet(0)
rows = workbook.sheets()[0].nrows

if_cluster = pd.read_csv('if_probability.csv')
original_if = pd.read_csv('if_dynamic_taken.csv')

original_if['probability'] = if_cluster['probability']

# with open('ifTotal','r') as f:
# 	for line in f.readlines():
# 		prob_data = line.split()
# 		if int(prob_data[4]) > 1000:
# 			for i in range(0, rows):
# 				if original_data.cell_value(i,0) == prob_data[1] and original_data.cell_value(i,1) == prob_data[2]:
# 					if original_data.cell_value(i,6) == 'Equal' or original_data.cell_value(i,6) == 'Larger' \
# 							or original_data.cell_value(i,6) == 'Smaller':
# 						res = 1 - float(prob_data[8])
# 						if res > 0.99:
# 							data.write(i, 9, 10000)
# 						else:
# 							data.write(i, 9, res)
# 					else:
# 						res = float(prob_data[8])
# 						if res > 0.99:
# 							data.write(i, 9, 10000)
# 						else:
# 							data.write(i, 9, res)

for i in range(original_if.shape[0]):
	for j in range(0,rows):
		if_file = original_if.loc[i, 'file']
		if_line = original_if.loc[i, 'line']
		original_file = original_data.cell_value(j,0)
		original_line = original_data.cell_value(j,1)
		if original_data.cell_value(j, 0) == original_if.loc[i, 'file'] and original_data.cell_value(j, 1) == original_if.loc[i, 'line']:
			if original_data.cell_value(j, 2) == '==' or original_data.cell_value(j, 2) == '>' \
					or original_data.cell_value(j, 2) == '<':
				res1 = 1/float(original_if.loc[i, 'probability'])
				res2 = 1/(1-(float(original_if.loc[i, 'probability'])))

				data.write(j, 9, res1)
				data.write(j, 10, res2)

			else:
				res1 = 1/(1-(float(original_if.loc[i, 'probability'])))
				res2 = 1/float(original_if.loc[i, 'probability'])
				data.write(j, 9, res1)
				data.write(j, 10, res2)


# for i in range(1, rows):
# 	if original_data.cell_value(i, 9):
# 		pass
# 	else:
# 		similar_if = original_data.cell_value(i, 8)[1:-1]
# 		similar_if_list = similar_if.split(',')
# 		for j in similar_if_list:
# 			if int(j)+2 < rows and original_data.cell_value(int(j)+2, 9):
# 				data.write(i, 9, original_data.cell_value(int(j)+2, 9))

excel.save("If with Probability.xls")