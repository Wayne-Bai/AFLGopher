import xlrd
import pandas as pd
import csv
import re
from xlutils.copy import copy

wb = xlrd.open_workbook("data.xls", formatting_info=True)

print( "sheet number:", wb.nsheets)

print( "sheet name:", wb.sheet_names())

sh1 = wb.sheet_by_index(0)
copy_sheet = copy(wb)
sheet_data = copy_sheet.get_sheet(0)

row_num = sh1.nrows
col_num = sh1.ncols
print( u"sheet %s total %d row %d column" % (sh1.name, sh1.nrows, sh1.ncols))

with open('if_data.csv', 'a') as w:

    writer = csv.writer(w)

    writer.writerow(["file", "line", "source 1", 'source 2', 'source 3'])

    if_index = 0

    for i in range(row_num):

        if if_index > 0:
            if sh1.cell_value(if_index, 3) != 'unknown' and sh1.cell_value(if_index, 8) != 'unknown' \
                    and sh1.cell_value(if_index, 13) != 'unknown':
                temp = []
                temp.append(sh1.cell_value(i,0))
                temp.append(sh1.cell_value(i,1))

                if sh1.cell_value(if_index, 7) and sh1.cell_value(if_index, 7) != 'unprecessed' and '_' in sh1.cell_value(if_index, 7):
                    temp.append(sh1.cell_value(if_index, 7))
                elif sh1.cell_value(if_index, 7) != 'unprecessed':
                    temp.append('N/A')

                if sh1.cell_value(if_index, 12) and sh1.cell_value(if_index, 12) != 'unprecessed' and '_' in sh1.cell_value(if_index, 12):
                    temp.append(sh1.cell_value(if_index, 12))
                elif sh1.cell_value(if_index, 12) != 'unprecessed':
                    temp.append('N/A')

                if sh1.cell_value(if_index, 17) and sh1.cell_value(if_index, 17) != 'unprecessed' and '_' in sh1.cell_value(if_index, 17):
                    temp.append(sh1.cell_value(if_index, 17))
                elif sh1.cell_value(if_index, 17) != 'unprecessed':
                    temp.append('N/A')

                writer.writerow(temp)
        if_index += 1

w.close()

