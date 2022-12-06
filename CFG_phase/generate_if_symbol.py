from xlrd import open_workbook
from xlutils.copy import copy
import pandas as pd

workbook = open_workbook('data.xls')
original_data = workbook.sheet_by_index(0)
excel = copy(workbook)
data = excel.get_sheet(0)
rows = workbook.sheets()[0].nrows

original_if = pd.read_csv('if_data.csv')

original_if['symbol'] = ''


for i in range(original_if.shape[0]):
    for j in range(0,rows):
        if_file = original_if.loc[i, 'file']
        if_line = original_if.loc[i, 'line']
        original_file = original_data.cell_value(j,0)
        original_line = original_data.cell_value(j,1)
        if original_data.cell_value(j, 0) == original_if.loc[i, 'file'] and original_data.cell_value(j, 1) == original_if.loc[i, 'line']:
            original_if.loc[i, 'symbol'] = original_data.cell_value(j, 2)

original_if.to_csv('if_symbol.csv')