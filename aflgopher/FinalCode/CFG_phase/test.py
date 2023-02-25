import re
# print(re.findall('[A-Z][^A-Z]*', 'TheLongAndWindingRoad'))
# print(re.findall('[a-z]+|[A-Z][^A-Z]*', 'theLongAndWindingRoad'))
#
# a = 'link_transition(t_transition* t ,t_state* from ,t_state* to )'
# b = re.split(r'[_,()\s]\s*',a)
# print(b)

# a = [1,2,3,4,5]
# print(a[:, 1])

# import xlrd
#
# wb = xlrd.open_workbook("test_verson.xls")
# # 获取并打印 sheet 数量
# print( "sheet number:", wb.nsheets)
# # 获取并打印 sheet 名称
# print( "sheet name:", wb.sheet_names())
# # 根据 sheet 索引获取内容
# sh1 = wb.sheet_by_index(0)
#
# sh1.put_cell(1, 1, 1, 'total_string', 0)

# from xlrd import open_workbook
# from xlutils.copy import copy
#
# # 用 xlrd 提供的方法读取一个excel文件
# rexcel = open_workbook("test_verson.xls",formatting_info=True) # 保留原有样式
# # 用 xlrd 提供的方法获得现在已有的行数
# rows = rexcel.sheets()[0].nrows
# # 用 xlutils 提供的copy方法将 xlrd 的对象转化为 xlwt 的对象
# excel = copy(rexcel)
# # 用 xlwt 对象的方法获得要操作的 sheet
# table = excel.get_sheet(0)
# values = ["1", "2", "3"]
# row = rows
# for value in values:
#     table.write(row, 0, value) # xlwt对象的写方法，参数分别是行、列、值
#     table.write(row, 1, "haha")
#     table.write(row, 2, "lala")
#     row += 1
# excel.save("test_verson.xls") # xlwt 对象的保存方法，这时便覆盖掉了原来的 Excel

# with open('test.txt', 'r') as f:
#     for line in f.readlines():
#         flag = 0
#         for i in line:
#             if i != ',':
#                 if i == '1':
#                     print(flag)
#                 flag+=1

# print("hello")
# a = [1,2,4]
# b = [9,8,7]
#
# c = a+b
# print("hello world")
# print(c)

import pandas as pd
data = pd.read_csv('function_cluster.csv')
print(data['label'].max())
print(data['label'].min())