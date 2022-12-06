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


global_type = ['i32', 'i64', 'i8*']

with open('global.csv', 'a') as w1:
    with open('function.csv', 'a') as w2:
        with open('argument.csv', 'a') as w3:
            writer1 = csv.writer(w1)
            writer2 = csv.writer(w2)
            writer3 = csv.writer(w3)

            writer1.writerow(["index", "type", "value", 'combination'])
            writer2.writerow(["index", "type", "value", 'combination'])
            writer3.writerow(["index", "type", "value", 'combination'])

            global_index = 0
            function_index = 0
            argument_index = 0

            for i in range(row_num):

                if i > 0:
                    if sh1.cell_value(i, 3) == 'global':
                        temp = []
                        temp.append(global_index)
                        temp.append(sh1.cell_value(i,4))
                        temp.append(sh1.cell_value(i,5))
                        # temp.append(sh1.cell_value(i,4) + '' + sh1.cell_value(i,5))
                        val_type = sh1.cell_value(i,4)
                        val_name = sh1.cell_value(i,5)

                        type_is_lower = [c.islower() for c in val_type]
                        name_is_lower = [c.islower() for c in val_name]
                        total_string = ''

                        if all(type_is_lower) or val_type in global_type:
                            if '_' in val_type:
                                type_list = val_type.split('_')
                                for frag in type_list:
                                    if frag != '':
                                        total_string += frag
                                        total_string += '\t'
                            else:
                                total_string += val_type
                                total_string += '\t'
                        else:
                            type_cap_list = re.findall('[a-z]+|[A-Z][^A-Z]*', val_type)
                            for frag in type_cap_list:
                                if '_' in frag:
                                    type_list = frag.split('_')
                                    for frag_frag in type_list:
                                        if frag_frag != '':
                                            total_string += frag_frag
                                            total_string += '\t'
                                else:
                                    if frag != '':
                                        total_string += frag
                                        total_string += '\t'

                        if all(name_is_lower):
                            if '_' in val_name:
                                name_list = val_name.split('_')
                                for frag in name_list:
                                    if frag != '':
                                        total_string += frag
                                        total_string += '\t'
                            else:
                                total_string += val_name
                                total_string += '\t'
                        elif all(type_is_lower) or val_type in global_type:
                            total_string += 'constant'
                            total_string += '\t'
                        else:
                            name_cap_list = re.findall('[a-z]+|[A-Z][^A-Z]*', val_type)
                            for frag in name_cap_list:
                                if '_' in frag:
                                    name_list = frag.split('_')
                                    for frag_frag in name_list:
                                        if frag_frag != '':
                                            total_string += frag_frag
                                            total_string += '\t'
                                else:
                                    if frag != '':
                                        total_string += frag
                                        total_string += '\t'

                        temp.append(total_string)
                        writer1.writerow(temp)
                        sheet_data.write(i, 6, total_string)
                        global_index += 1
                    if sh1.cell_value(i, 8) == 'global':
                        temp = []
                        temp.append(global_index)
                        temp.append(sh1.cell_value(i,9))
                        temp.append(sh1.cell_value(i,10))
                        # temp.append(sh1.cell_value(i,7) + '' + sh1.cell_value(i,8))
                        val_type = sh1.cell_value(i, 9)
                        val_name = sh1.cell_value(i, 10)

                        type_is_lower = [c.islower() for c in val_type]
                        name_is_lower = [c.islower() for c in val_name]
                        total_string = ''

                        if all(type_is_lower) or val_type in global_type:
                            if '_' in val_type:
                                type_list = val_type.split('_')
                                for frag in type_list:
                                    if frag != '':
                                        total_string += frag
                                        total_string += '\t'
                            else:
                                total_string += val_type
                                total_string += '\t'
                        else:
                            type_cap_list = re.findall('[a-z]+|[A-Z][^A-Z]*', val_type)
                            for frag in type_cap_list:
                                if '_' in frag:
                                    type_list = frag.split('_')
                                    for frag_frag in type_list:
                                        if frag_frag != '':
                                            total_string += frag_frag
                                            total_string += '\t'
                                else:
                                    if frag != '':
                                        total_string += frag
                                        total_string += '\t'

                        if all(name_is_lower):
                            if '_' in val_name:
                                name_list = val_name.split('_')
                                for frag in name_list:
                                    if frag != '':
                                        total_string += frag
                                        total_string += '\t'
                            else:
                                total_string += val_name
                                total_string += '\t'
                        elif all(type_is_lower) or val_type in global_type:
                            total_string += 'constant'
                            total_string += '\t'
                        else:
                            name_cap_list = re.findall('[a-z]+|[A-Z][^A-Z]*', val_name)
                            for frag in name_cap_list:
                                if '_' in frag:
                                    name_list = frag.split('_')
                                    for frag_frag in name_list:
                                        if frag_frag != '':
                                            total_string += frag_frag
                                            total_string += '\t'
                                else:
                                    if frag != '':
                                        total_string += frag
                                        total_string += '\t'

                        temp.append(total_string)
                        writer1.writerow(temp)
                        sheet_data.write(i, 11, total_string)
                        global_index += 1
                    if sh1.cell_value(i, 13) == 'global':
                        temp = []
                        temp.append(global_index)
                        temp.append(sh1.cell_value(i,14))
                        temp.append(sh1.cell_value(i,15))
                        # temp.append(sh1.cell_value(i,10) + '' + sh1.cell_value(i,11))
                        val_type = sh1.cell_value(i, 14)
                        val_name = sh1.cell_value(i, 15)

                        type_is_lower = [c.islower() for c in val_type]
                        name_is_lower = [c.islower() for c in val_name]
                        total_string = ''

                        if all(type_is_lower) or val_type in global_type:
                            if '_' in val_type:
                                type_list = val_type.split('_')
                                for frag in type_list:
                                    if frag != '':
                                        total_string += frag
                                        total_string += '\t'
                            else:
                                total_string += val_type
                                total_string += '\t'
                        else:
                            type_cap_list = re.findall('[a-z]+|[A-Z][^A-Z]*', val_type)
                            for frag in type_cap_list:
                                if '_' in frag:
                                    type_list = frag.split('_')
                                    for frag_frag in type_list:
                                        if frag_frag != '':
                                            total_string += frag_frag
                                            total_string += '\t'
                                else:
                                    if frag != '':
                                        total_string += frag
                                        total_string += '\t'

                        if all(name_is_lower):
                            if '_' in val_name:
                                name_list = val_name.split('_')
                                for frag in name_list:
                                    if frag != '':
                                        total_string += frag
                                        total_string += '\t'
                            else:
                                total_string += val_name
                                total_string += '\t'
                        elif all(type_is_lower) or val_type in global_type:
                            total_string += 'constant'
                            total_string += '\t'
                        else:
                            name_cap_list = re.findall('[a-z]+|[A-Z][^A-Z]*', val_name)
                            for frag in name_cap_list:
                                if '_' in frag:
                                    name_list = frag.split('_')
                                    for frag_frag in name_list:
                                        if frag_frag != '':
                                            total_string += frag_frag
                                            total_string += '\t'
                                else:
                                    if frag != '':
                                        total_string += frag
                                        total_string += '\t'

                        temp.append(total_string)
                        writer1.writerow(temp)
                        sheet_data.write(i, 16, total_string)
                        global_index += 1

                    if sh1.cell_value(i, 3) == 'function':
                        temp = []
                        temp.append(function_index)
                        temp.append(sh1.cell_value(i,4))
                        temp.append(sh1.cell_value(i,5))
                        # temp.append(sh1.cell_value(i,4) + '' + sh1.cell_value(i,5))

                        val_type = sh1.cell_value(i, 4)
                        val_name = sh1.cell_value(i, 5)

                        type_is_lower = [c.islower() for c in val_type]
                        name_is_lower = [c.islower() for c in val_name]
                        total_string = ''

                        if all(type_is_lower) or val_type in global_type:
                            if '_' in val_type:
                                type_list = val_type.split('_')
                                for frag in type_list:
                                    if frag != '':
                                        total_string += frag
                                        total_string += '\t'
                            else:
                                total_string += val_type
                                total_string += '\t'
                        else:
                            type_cap_list = re.findall('[a-z]+|[A-Z][^A-Z]*', val_type)
                            for frag in type_cap_list:
                                if '_' in frag:
                                    type_list = frag.split('_')
                                    for frag_frag in type_list:
                                        if frag_frag != '':
                                            total_string += frag_frag
                                            total_string += '\t'
                                else:
                                    if frag != '':
                                        total_string += frag
                                        total_string += '\t'

                        if all(name_is_lower):
                            if '_' in val_name:
                                name_list = val_name.split('_')
                                for frag in name_list:
                                    if frag != '':
                                        total_string += frag
                                        total_string += '\t'
                            else:
                                total_string += val_name
                                total_string += '\t'
                        else:
                            name_cap_list = re.findall('[a-z]+|[A-Z][^A-Z]*', val_name)
                            for frag in name_cap_list:
                                if '_' in frag:
                                    name_list = frag.split('_')
                                    for frag_frag in name_list:
                                        if frag_frag != '':
                                            total_string += frag_frag
                                            total_string += '\t'
                                else:
                                    if frag != '':
                                        total_string += frag
                                        total_string += '\t'

                        temp.append(total_string)
                        writer2.writerow(temp)
                        sheet_data.write(i, 6, total_string)
                        function_index += 1

                    if sh1.cell_value(i, 8) == 'function':
                        temp = []
                        temp.append(function_index)
                        temp.append(sh1.cell_value(i,9))
                        temp.append(sh1.cell_value(i,10))
                        # temp.append(sh1.cell_value(i,7) + '' + sh1.cell_value(i,8))

                        val_type = sh1.cell_value(i, 9)
                        val_name = sh1.cell_value(i, 10)

                        type_is_lower = [c.islower() for c in val_type]
                        name_is_lower = [c.islower() for c in val_name]
                        total_string = ''

                        if all(type_is_lower) or val_type in global_type:
                            if '_' in val_type:
                                type_list = val_type.split('_')
                                for frag in type_list:
                                    if frag != '':
                                        total_string += frag
                                        total_string += '\t'
                            else:
                                total_string += val_type
                                total_string += '\t'
                        else:
                            type_cap_list = re.findall('[a-z]+|[A-Z][^A-Z]*', val_type)
                            for frag in type_cap_list:
                                if '_' in frag:
                                    type_list = frag.split('_')
                                    for frag_frag in type_list:
                                        if frag_frag != '':
                                            total_string += frag_frag
                                            total_string += '\t'
                                else:
                                    if frag != '':
                                        total_string += frag
                                        total_string += '\t'

                        if all(name_is_lower):
                            if '_' in val_name:
                                name_list = val_name.split('_')
                                for frag in name_list:
                                    if frag != '':
                                        total_string += frag
                                        total_string += '\t'
                            else:
                                total_string += val_name
                                total_string += '\t'
                        else:
                            name_cap_list = re.findall('[a-z]+|[A-Z][^A-Z]*', val_name)
                            for frag in name_cap_list:
                                if '_' in frag:
                                    name_list = frag.split('_')
                                    for frag_frag in name_list:
                                        if frag_frag != '':
                                            total_string += frag_frag
                                            total_string += '\t'
                                else:
                                    if frag != '':
                                        total_string += frag
                                        total_string += '\t'

                        temp.append(total_string)
                        sheet_data.write(i, 11, total_string)
                        writer2.writerow(temp)
                        function_index += 1

                    if sh1.cell_value(i, 13) == 'function':
                        temp = []
                        temp.append(function_index)
                        temp.append(sh1.cell_value(i,14))
                        temp.append(sh1.cell_value(i,15))
                        # temp.append(sh1.cell_value(i,10) + '' + sh1.cell_value(i,11))

                        val_type = sh1.cell_value(i, 14)
                        val_name = sh1.cell_value(i, 15)

                        type_is_lower = [c.islower() for c in val_type]
                        name_is_lower = [c.islower() for c in val_name]
                        total_string = ''

                        if all(type_is_lower) or val_type in global_type:
                            if '_' in val_type:
                                type_list = val_type.split('_')
                                for frag in type_list:
                                    if frag != '':
                                        total_string += frag
                                        total_string += '\t'
                            else:
                                total_string += val_type
                                total_string += '\t'
                        else:
                            type_cap_list = re.findall('[a-z]+|[A-Z][^A-Z]*', val_type)
                            for frag in type_cap_list:
                                if '_' in frag:
                                    type_list = frag.split('_')
                                    for frag_frag in type_list:
                                        if frag_frag != '':
                                            total_string += frag_frag
                                            total_string += '\t'
                                else:
                                    if frag != '':
                                        total_string += frag
                                        total_string += '\t'

                        if all(name_is_lower) or val_type in global_type:
                            if '_' in val_name:
                                name_list = val_name.split('_')
                                for frag in name_list:
                                    if frag != '':
                                        total_string += frag
                                        total_string += '\t'
                            else:
                                total_string += val_name
                                total_string += '\t'
                        else:
                            name_cap_list = re.findall('[a-z]+|[A-Z][^A-Z]*', val_name)
                            for frag in name_cap_list:
                                if '_' in frag:
                                    name_list = frag.split('_')
                                    for frag_frag in name_list:
                                        if frag_frag != '':
                                            total_string += frag_frag
                                            total_string += '\t'
                                else:
                                    if frag != '':
                                        total_string += frag
                                        total_string += '\t'

                        temp.append(total_string)
                        sheet_data.write(i, 16, total_string)
                        writer2.writerow(temp)
                        function_index += 1
                    if sh1.cell_value(i, 3) == 'argument':
                        temp = []
                        temp.append(argument_index)
                        temp.append(sh1.cell_value(i,4))
                        temp.append(sh1.cell_value(i,5))
                        # temp.append(sh1.cell_value(i,4) + '' + sh1.cell_value(i,5))

                        val_type = sh1.cell_value(i, 4)
                        val_name = sh1.cell_value(i, 5)

                        type_is_lower = [c.islower() for c in val_type]
                        # name_is_lower = [c.islower() for c in val_name]
                        temp_name_split_list = re.split(r'[_,()\s]\s*', val_name)
                        name_split_list = [x for x in temp_name_split_list if x != '']
                        total_string = ''

                        if all(type_is_lower) or val_type in global_type:
                            if '_' in val_type:
                                type_list = val_type.split('_')
                                for frag in type_list:
                                    if frag != '':
                                        total_string += frag
                                        total_string += '\t'
                            else:
                                total_string += val_type
                                total_string += '\t'
                        else:
                            type_cap_list = re.findall('[a-z]+|[A-Z][^A-Z]*', val_type)
                            for frag in type_cap_list:
                                if '_' in frag:
                                    type_list = frag.split('_')
                                    for frag_frag in type_list:
                                        if frag_frag != '':
                                            total_string += frag_frag
                                            total_string += '\t'
                                else:
                                    if frag != '':
                                        total_string += frag
                                        total_string += '\t'

                        for name in name_split_list:
                            name_is_lower = [c.islower() for c in name]
                            if all(name_is_lower) or name in global_type:
                                if '_' in name:
                                    name_list = name.split('_')
                                    for frag in name_list:
                                        if frag != '':
                                            total_string += frag
                                            total_string += '\t'
                                else:
                                    total_string += name
                                    total_string += '\t'
                            else:
                                name_cap_list = re.findall('[a-z]+|[A-Z][^A-Z]*', name)
                                for frag in name_cap_list:
                                    if '_' in frag:
                                        name_list = frag.split('_')
                                        for frag_frag in name_list:
                                            if frag_frag != '':
                                                total_string += frag_frag
                                                total_string += '\t'
                                    else:
                                        if frag != '':
                                            total_string += frag
                                            total_string += '\t'

                        temp.append(total_string)
                        writer3.writerow(temp)
                        sheet_data.write(i, 6, total_string)
                        argument_index += 1

                    if sh1.cell_value(i, 8) == 'argument':
                        temp = []
                        temp.append(argument_index)
                        temp.append(sh1.cell_value(i,9))
                        temp.append(sh1.cell_value(i,10))
                        # temp.append(sh1.cell_value(i,7) + '' + sh1.cell_value(i,8))

                        val_type = sh1.cell_value(i, 9)
                        val_name = sh1.cell_value(i, 10)

                        type_is_lower = [c.islower() for c in val_type]
                        # name_is_lower = [c.islower() for c in val_name]
                        temp_name_split_list = re.split(r'[_,()\s]\s*', val_name)
                        name_split_list = [x for x in temp_name_split_list if x != '']
                        total_string = ''

                        if all(type_is_lower) or val_type in global_type:
                            if '_' in val_type:
                                type_list = val_type.split('_')
                                for frag in type_list:
                                    if frag != '':
                                        total_string += frag
                                        total_string += '\t'
                            else:
                                total_string += val_type
                                total_string += '\t'
                        else:
                            type_cap_list = re.findall('[a-z]+|[A-Z][^A-Z]*', val_type)
                            for frag in type_cap_list:
                                if '_' in frag:
                                    type_list = frag.split('_')
                                    for frag_frag in type_list:
                                        if frag_frag != '':
                                            total_string += frag_frag
                                            total_string += '\t'
                                else:
                                    if frag != '':
                                        total_string += frag
                                        total_string += '\t'

                        for name in name_split_list:
                            name_is_lower = [c.islower() for c in name]
                            if all(name_is_lower) or name in global_type:
                                if '_' in name:
                                    name_list = name.split('_')
                                    for frag in name_list:
                                        if frag != '':
                                            total_string += frag
                                            total_string += '\t'
                                else:
                                    total_string += name
                                    total_string += '\t'
                            else:
                                name_cap_list = re.findall('[a-z]+|[A-Z][^A-Z]*', name)
                                for frag in name_cap_list:
                                    if '_' in frag:
                                        name_list = frag.split('_')
                                        for frag_frag in name_list:
                                            if frag_frag != '':
                                                total_string += frag_frag
                                                total_string += '\t'
                                    else:
                                        if frag != '':
                                            total_string += frag
                                            total_string += '\t'

                        temp.append(total_string)
                        writer3.writerow(temp)
                        sheet_data.write(i, 11, total_string)
                        argument_index += 1

                    if sh1.cell_value(i, 13) == 'argument':
                        temp = []
                        temp.append(argument_index)
                        temp.append(sh1.cell_value(i,14))
                        temp.append(sh1.cell_value(i,15))
                        # temp.append(sh1.cell_value(i,10) + '' + sh1.cell_value(i,11))

                        val_type = sh1.cell_value(i, 14)
                        val_name = sh1.cell_value(i, 15)

                        type_is_lower = [c.islower() for c in val_type]
                        # name_is_lower = [c.islower() for c in val_name]
                        temp_name_split_list = re.split(r'[_,()\s]\s*', val_name)
                        name_split_list = [x for x in temp_name_split_list if x != '']
                        total_string = ''

                        if all(type_is_lower) or val_type in global_type:
                            if '_' in val_type:
                                type_list = val_type.split('_')
                                for frag in type_list:
                                    if frag != '':
                                        total_string += frag
                                        total_string += '\t'
                            else:
                                total_string += val_type
                                total_string += '\t'
                        else:
                            type_cap_list = re.findall('[a-z]+|[A-Z][^A-Z]*', val_type)
                            for frag in type_cap_list:
                                if '_' in frag:
                                    type_list = frag.split('_')
                                    for frag_frag in type_list:
                                        if frag_frag != '':
                                            total_string += frag_frag
                                            total_string += '\t'
                                else:
                                    if frag != '':
                                        total_string += frag
                                        total_string += '\t'

                        for name in name_split_list:
                            name_is_lower = [c.islower() for c in name]
                            if all(name_is_lower) or name in global_type:
                                if '_' in name:
                                    name_list = name.split('_')
                                    for frag in name_list:
                                        if frag != '':
                                            total_string += frag
                                            total_string += '\t'
                                else:
                                    total_string += name
                                    total_string += '\t'
                            else:
                                name_cap_list = re.findall('[a-z]+|[A-Z][^A-Z]*', name)
                                for frag in name_cap_list:
                                    if '_' in frag:
                                        name_list = frag.split('_')
                                        for frag_frag in name_list:
                                            if frag_frag != '':
                                                total_string += frag_frag
                                                total_string += '\t'
                                    else:
                                        if frag != '':
                                            total_string += frag
                                            total_string += '\t'

                        temp.append(total_string)
                        writer3.writerow(temp)
                        sheet_data.write(i, 6, total_string)
                        argument_index += 1
w1.close()
w2.close()
w3.close()
copy_sheet.save("data.xls")