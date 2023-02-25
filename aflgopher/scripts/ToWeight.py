#!/usr/bin/env python
# coding: utf-8

# In[1]:


import xlrd
import xlwt


# In[2]:


filePath="Final IF.xls"
x1 = xlrd.open_workbook(filePath)
sheet1 = x1.sheet_by_name("IF statement")




# create weight sheet
workbook = xlwt.Workbook()
sheet = workbook.add_sheet("data")

header_font = xlwt.Font()
header_font.name = 'Arial'
header_font.bold = True
header_style = xlwt.XFStyle()
header_style.font = header_font

sheet.write(0, 0, 'file', header_style)
sheet.write(0, 1, 'BB', header_style)
sheet.write(0, 2, 'BB_next', header_style)
sheet.write(0, 3, 'weight', header_style)
sheet.write(0, 4, 'false_weight', header_style)

row=1
for index in range(1,sheet1.nrows):
    file_name=sheet1.cell_value(index, 0)
    file_line=sheet1.cell_value(index, 1)
    file_weight=sheet1.cell_value(index, 9)
    false_weight=sheet1.cell_value(index, 10)
    if (file_weight==""):
        continue
    f = open("ifLookUp")
    allIf = f.readlines()
    
    for record in allIf:
        match=record.split(' ')
        file_if=match[1]
        line_if=int(match[2])
        BB_if=int(match[4])
        next_if=int(match[6])
        if (file_name==file_if and int(file_line.rstrip("+"))==line_if):
                sheet.write(row, 0, file_name)
                sheet.write(row, 1, BB_if)
                sheet.write(row, 2, next_if)
                sheet.write(row, 3, file_weight)
                sheet.write(row, 4, false_weight)
                row=row+1
    print(index)
workbook.save('weight.xls')


# In[ ]:




