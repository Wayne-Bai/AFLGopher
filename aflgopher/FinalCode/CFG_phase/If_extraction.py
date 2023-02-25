import xlwt

# TODO: generate c file list
c_file_list = []

with open('address.txt','r') as f:
    for line in f.readlines():
        if line.strip():
            c_file_list.append(line.strip())

f.close()
#
# # print(c_file_list)
# # print(len(c_file_list))

# generate sheet
workbook = xlwt.Workbook(encoding='utf-8')
worksheet = workbook.add_sheet('IF statement', cell_overwrite_ok=True)

# add HEAD
worksheet.write(0, 0, label='IF statement')
worksheet.write(0, 1, label='Global Operator')
worksheet.write(0, 2, label='Value')
worksheet.write(0, 3, label='Left Value')
worksheet.write(0, 4, label='Right Value')
worksheet.write(0, 5, label='Operator')
worksheet.write(0, 6, label='Category')
worksheet.write(0, 7, label='Branch Possibility')
worksheet.write(0, 8, label='File Name')
worksheet.write(0, 9, label='Line')
worksheet.write(0, 10, label='Source 1 From')
worksheet.write(0, 11, label='Source 1 Type')
worksheet.write(0, 12, label='Source 1 Info')
worksheet.write(0, 13, label='Source 2 From')
worksheet.write(0, 14, label='Source 2 Type')
worksheet.write(0, 15, label='Source 2 Info')
worksheet.write(0, 16, label='Source 3 From')
worksheet.write(0, 17, label='Source 3 Type')
worksheet.write(0, 18, label='Source 3 Info')

# TODO: test case => buf.c
# with open('libxml2/buf.c', 'r') as f1:
#
#     line_num = 0
#     if_stmt_list = []
#     if_statement = ''
#     num_bracket = 0
#     if_stmt_dict = {}
#     if_stmt_dict['file_name'] = 'libxml2/buf.c'
#     if_stmt_dict['line'] = []
#     if_dict_list = []
#     final_list = []
#     val = 1
#
#     for code in f1.readlines():
#         line_num += 1
#         if 'if (' in code:
#             if_statement = code.strip()
#             if_stmt_dict['line'].append(line_num)
#             for i in code.strip():
#                 if i == '(':
#                     num_bracket += 1
#                 elif i == ')':
#                     num_bracket -= 1
#
#             if num_bracket == 0:
#                 if_stmt_list.append(if_statement)
#                 if_stmt_dict['statement'] = if_statement
#                 if_dict_list.append(if_stmt_dict.copy())
#                 if_stmt_dict['line'] = []
#
#         elif 'if (' not in code and num_bracket != 0:
#             if_statement += code.strip()
#             if_stmt_dict['line'].append(line_num)
#             for i in code.strip():
#                 if i == '(':
#                     num_bracket += 1
#                 elif i == ')':
#                     num_bracket -= 1
#             if num_bracket == 0:
#                 if_stmt_list.append(if_statement)
#                 if_stmt_dict['statement'] = if_statement
#                 if_statement = ''
#                 if_dict_list.append(if_stmt_dict.copy())
#                 if_stmt_dict['line'] = []
#
#     for i in if_dict_list:
#         if '&&' in i['statement'] or '||' in i['statement']:
#             and_number = i['statement'].count('&&')
#             or_number = i['statement'].count('||')
#             i['Global operator'] = []
#             result = []
#             if and_number != 0:
#                 i['Global operator'].extend(['&&' for x in range(and_number)])
#                 result = i['statement'].split('&&')
#             if or_number != 0:
#                 i['Global operator'].extend(['||' for x in range(or_number)])
#                 if result == []:
#                     result = i['statement'].split('||')
#                 else:
#                     for res in result.copy():
#                         if '||' in res:
#                             result.extend(res.split('||'))
#             i['split statement'] = result
#
#
#     for dic in if_dict_list:
#         if 'split statement' in dic.keys():
#             final_list.append(dic)
#             temp = {}
#             temp['file_name'] = dic['file_name']
#             temp['line'] = dic['line']
#             for j in dic['split statement']:
#                 temp['statement'] = j
#                 final_list.append(temp.copy())
#         else:
#             final_list.append(dic)
#
#     # worksheet.write(0, 0, label='IF statement')
#     # worksheet.write(0, 1, label='Global Operator')
#     # worksheet.write(0, 2, label='Value')
#     # worksheet.write(0, 3, label='Left Value')
#     # worksheet.write(0, 4, label='Right Value')
#     # worksheet.write(0, 5, label='Operator')
#     # worksheet.write(0, 6, label='Category')
#     # worksheet.write(0, 7, label='Branch Possibility')
#     # worksheet.write(0, 8, label='File Name')
#     # worksheet.write(0, 9, label='Line')
#
#     for i in final_list:
#         if 'Global operator' in i.keys():
#             worksheet.write(val, 0, i['statement'])
#             worksheet.write(val, 1, str(i['Global operator']))
#             worksheet.write(val, 8, i['file_name'])
#             worksheet.write(val, 9, str(i['line']))
#             val += 1
#         else:
#             worksheet.write(val, 0, i['statement'])
#             worksheet.write(val, 8, i['file_name'])
#             worksheet.write(val, 9, str(i['line']))
#
#             first_bracket = 0
#             second_bracket = 0
#             total_bracket = 0
#             right_bracket = 0
#             last_bracket = 0
#
#             for j in range(len(i['statement'])):
#                 # if i['statement'][j] == '(' and total_bracket == 0:
#                 #     first_bracket = j
#                 #     total_bracket += 1
#                 # elif i['statement'][j] == '(':
#                 #     total_bracket += 1
#                 # elif i['statement'][j] == ')':
#                 #     total_bracket -= 1
#                 #     if total_bracket == 0:
#                 #         last_bracket = j
#                 if i['statement'][j] == '(' and total_bracket == 0:
#                     first_bracket = j
#                     total_bracket += 1
#                 elif i['statement'][j] == '(' and total_bracket == 1:
#                     second_bracket = j
#                     total_bracket += 1
#                 elif i['statement'][j] == '(':
#                     total_bracket += 1
#                 elif i['statement'][j] == ')':
#                     total_bracket -= 1
#                     right_bracket = j
#                     if total_bracket == 0:
#                         last_bracket = j
#                 elif j == len(i['statement'])-1 and total_bracket == 1:
#                     last_bracket = right_bracket
#                     first_bracket = second_bracket
#             value = i['statement'][first_bracket+1:last_bracket]
#
#             worksheet.write(val, 2, value)
#
#             if '==' in value:
#                 worksheet.write(val, 3, value.split('==')[0].strip())
#                 worksheet.write(val, 4, value.split('==')[1].strip())
#                 worksheet.write(val, 5, '==')
#                 worksheet.write(val, 6, 'check specific value')
#             elif '!=' in value:
#                 worksheet.write(val, 3, value.split('!=')[0].strip())
#                 worksheet.write(val, 4, value.split('!=')[1].strip())
#                 worksheet.write(val, 5, '!=')
#                 worksheet.write(val, 6, 'check specific value')
#             elif ' > ' in value and '=' not in value:
#                 worksheet.write(val, 3, value.split(' > ')[0].strip())
#                 worksheet.write(val, 4, value.split(' > ')[1].strip())
#                 worksheet.write(val, 5, '>')
#                 worksheet.write(val, 6, 'larger than specific value')
#             elif ' < ' in value and '=' not in value:
#                 worksheet.write(val, 3, value.split(' < ')[0].strip())
#                 worksheet.write(val, 4, value.split(' < ')[1].strip())
#                 worksheet.write(val, 5, '<')
#                 worksheet.write(val, 6, 'larger than specific value')
#             elif '>=' in value:
#                 worksheet.write(val, 3, value.split('>=')[0].strip())
#                 worksheet.write(val, 4, value.split('>=')[1].strip())
#                 worksheet.write(val, 5, '>=')
#                 worksheet.write(val, 6, 'larger than specific value')
#             elif '<=' in value:
#                 worksheet.write(val, 3, value.split('<=')[0].strip())
#                 worksheet.write(val, 4, value.split('<=')[1].strip())
#                 worksheet.write(val, 5, '<=')
#                 worksheet.write(val, 6, 'larger than specific value')
#             elif '!' in value:
#                 worksheet.write(val, 4, value.split('!')[1].strip())
#                 worksheet.write(val, 5, '!')
#                 worksheet.write(val, 6, 'check specific value')
#             else:
#                 worksheet.write(val, 3, value.strip())
#                 worksheet.write(val, 6, 'check specific value')
#
#             val += 1
#
# # save file
# workbook.save('test_verson.xls')
#
# # check the output of extraction
# # for i in if_stmt_list:
# #     print(i)
# # print(len(if_stmt_list))
# # for i in if_dict_list:
# #     print(i)
# # print(len(if_dict_list))
# # for i in final_list:
# #     print(i)

# TODO: generate all if statement
val = 1

for name in c_file_list:
    with open(name, 'r') as f1:

        line_num = 0
        if_stmt_list = []
        if_statement = ''
        num_bracket = 0
        if_stmt_dict = {}
        if_stmt_dict['file_name'] = name
        if_stmt_dict['line'] = []
        if_dict_list = []
        final_list = []

        for code in f1.readlines():
            line_num += 1
            if 'if (' in code:
                if_statement = code.strip()
                if_stmt_dict['line'].append(line_num)
                for i in code.strip():
                    if i == '(':
                        num_bracket += 1
                    elif i == ')':
                        num_bracket -= 1

                if num_bracket == 0:
                    if_stmt_list.append(if_statement)
                    if_stmt_dict['statement'] = if_statement
                    if_dict_list.append(if_stmt_dict.copy())
                    if_stmt_dict['line'] = []

            elif 'if (' not in code and num_bracket != 0:
                if_statement += code.strip()
                if_stmt_dict['line'].append(line_num)
                for i in code.strip():
                    if i == '(':
                        num_bracket += 1
                    elif i == ')':
                        num_bracket -= 1
                if num_bracket == 0:
                    if_stmt_list.append(if_statement)
                    if_stmt_dict['statement'] = if_statement
                    if_statement = ''
                    if_dict_list.append(if_stmt_dict.copy())
                    if_stmt_dict['line'] = []

        for i in if_dict_list:
            if '&&' in i['statement'] or '||' in i['statement']:
                and_number = i['statement'].count('&&')
                or_number = i['statement'].count('||')
                i['Global operator'] = []
                result = []
                if and_number != 0:
                    i['Global operator'].extend(['&&' for x in range(and_number)])
                    result = i['statement'].split('&&')
                if or_number != 0:
                    i['Global operator'].extend(['||' for x in range(or_number)])
                    if result == []:
                        result = i['statement'].split('||')
                    else:
                        for res in result.copy():
                            if '||' in res:
                                result.extend(res.split('||'))
                i['split statement'] = result


        for dic in if_dict_list:
            if 'split statement' in dic.keys():
                final_list.append(dic)
                temp = {}
                temp['file_name'] = dic['file_name']
                temp['line'] = dic['line']
                for j in dic['split statement']:
                    temp['statement'] = j
                    final_list.append(temp.copy())
            else:
                final_list.append(dic)

        # worksheet.write(0, 0, label='IF statement')
        # worksheet.write(0, 1, label='Global Operator')
        # worksheet.write(0, 2, label='Value')
        # worksheet.write(0, 3, label='Left Value')
        # worksheet.write(0, 4, label='Right Value')
        # worksheet.write(0, 5, label='Operator')
        # worksheet.write(0, 6, label='Category')
        # worksheet.write(0, 7, label='Branch Possibility')
        # worksheet.write(0, 8, label='File Name')
        # worksheet.write(0, 9, label='Line')

        for i in final_list:
            if 'Global operator' in i.keys():
                worksheet.write(val, 0, i['statement'])
                worksheet.write(val, 1, str(i['Global operator']))
                worksheet.write(val, 8, i['file_name'])
                worksheet.write(val, 9, str(i['line']))
                val += 1
            else:
                worksheet.write(val, 0, i['statement'])
                worksheet.write(val, 8, i['file_name'])
                worksheet.write(val, 9, str(i['line']))

                first_bracket = 0
                second_bracket = 0
                total_bracket = 0
                right_bracket = 0
                last_bracket = 0

                for j in range(len(i['statement'])):
                    # if i['statement'][j] == '(' and total_bracket == 0:
                    #     first_bracket = j
                    #     total_bracket += 1
                    # elif i['statement'][j] == '(':
                    #     total_bracket += 1
                    # elif i['statement'][j] == ')':
                    #     total_bracket -= 1
                    #     if total_bracket == 0:
                    #         last_bracket = j
                    if i['statement'][j] == '(' and total_bracket == 0:
                        first_bracket = j
                        total_bracket += 1
                    elif i['statement'][j] == '(' and total_bracket == 1:
                        second_bracket = j
                        total_bracket += 1
                    elif i['statement'][j] == '(':
                        total_bracket += 1
                    elif i['statement'][j] == ')':
                        total_bracket -= 1
                        right_bracket = j
                        if total_bracket == 0:
                            last_bracket = j
                    elif j == len(i['statement'])-1 and total_bracket == 1:
                        last_bracket = right_bracket
                        first_bracket = second_bracket
                value = i['statement'][first_bracket+1:last_bracket]

                worksheet.write(val, 2, value)

                if '==' in value:
                    worksheet.write(val, 3, value.split('==')[0].strip())
                    worksheet.write(val, 4, value.split('==')[1].strip())
                    worksheet.write(val, 5, '==')
                    worksheet.write(val, 6, 'check specific value')
                elif '!=' in value:
                    worksheet.write(val, 3, value.split('!=')[0].strip())
                    worksheet.write(val, 4, value.split('!=')[1].strip())
                    worksheet.write(val, 5, '!=')
                    worksheet.write(val, 6, 'check specific value')
                elif ' > ' in value and '=' not in value:
                    worksheet.write(val, 3, value.split(' > ')[0].strip())
                    worksheet.write(val, 4, value.split(' > ')[1].strip())
                    worksheet.write(val, 5, '>')
                    worksheet.write(val, 6, 'larger than specific value')
                elif ' < ' in value and '=' not in value:
                    worksheet.write(val, 3, value.split(' < ')[0].strip())
                    worksheet.write(val, 4, value.split(' < ')[1].strip())
                    worksheet.write(val, 5, '<')
                    worksheet.write(val, 6, 'larger than specific value')
                elif '>=' in value:
                    worksheet.write(val, 3, value.split('>=')[0].strip())
                    worksheet.write(val, 4, value.split('>=')[1].strip())
                    worksheet.write(val, 5, '>=')
                    worksheet.write(val, 6, 'larger than specific value')
                elif '<=' in value:
                    worksheet.write(val, 3, value.split('<=')[0].strip())
                    worksheet.write(val, 4, value.split('<=')[1].strip())
                    worksheet.write(val, 5, '<=')
                    worksheet.write(val, 6, 'larger than specific value')
                elif '!' in value:
                    worksheet.write(val, 4, value.split('!')[1].strip())
                    worksheet.write(val, 5, '!')
                    worksheet.write(val, 6, 'check specific value')
                else:
                    worksheet.write(val, 3, value.strip())
                    worksheet.write(val, 6, 'check specific value')

                val += 1

# save file
workbook.save('Total IF Statement.xls')
