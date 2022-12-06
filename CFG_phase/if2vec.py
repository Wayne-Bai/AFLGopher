import pandas as pd
import numpy as np
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--global_number", type=int, default=96)
parser.add_argument("--function_number", type=int, default=197)
parser.add_argument("--argument_number", type=int, default=614)

args = parser.parse_args()

global_cluster = args.global_number
function_cluster = args.function_number
argument_cluster = args.argument_number
total_number = global_cluster + function_cluster + argument_cluster

d = 3 * total_number + 9

file_name = args.category

data = pd.read_csv('if_data.csv')

frame_row, frame_shape = data.shape

whole_list = []

for i in range(frame_row):

    temp = [0 for x in range(d)] # larger than the combination of number of clusters of each categories

    if pd.isna(data.iat[i,2]) == False:


        s_type = data.iat[i,2].split('_')[0]
        s_cluster = data.iat[i,2].split('_')[1]

        if s_type == 'global':
            temp[0] = 1
            temp_index = int(s_cluster) + 2 + 2
            temp[temp_index] = 1

        elif s_type == 'function':
            temp[1] = 1
            temp_index = global_cluster + 2 + int(s_cluster) + 2
            temp[temp_index] = 1

        elif s_type == 'argument':
            temp[2] = 1
            temp_index = global_cluster + function_cluster + 2 + int(s_cluster) + 2
            temp[temp_index] = 1

    if pd.isna(data.iat[i,3]) == False:

        s_type = data.iat[i, 3].split('_')[0]
        s_cluster = data.iat[i, 3].split('_')[1]

        if s_type == 'global':
            temp[total_number+3] = 1
            temp_index = total_number + 3 + int(s_cluster) + 2 + 2
            temp[temp_index] = 1

        elif s_type == 'function':
            temp[total_number+4] = 1
            temp_index = total_number + 3 + global_cluster + 2 + int(s_cluster) +2
            temp[temp_index] = 1

        elif s_type == 'argument':
            temp[total_number+5] = 1
            temp_index = total_number + 3 + function_cluster + global_cluster + 2 + int(s_cluster) +2
            temp[temp_index] = 1

    if pd.isna(data.iat[i,4]) == False:

        s_type = data.iat[i, 4].split('_')[0]
        s_cluster = data.iat[i, 4].split('_')[1]

        if s_type == 'global':
            temp[2*total_number+6] = 1
            temp_index = 2 * total_number + 6 + int(s_cluster) + 2 + 2
            temp[temp_index] = 1

        elif s_type == 'function':
            temp[2*total_number+7] = 1
            temp_index = 2 * total_number + 6 + global_cluster + 2 + int(s_cluster) + 2
            temp[temp_index] = 1

        elif s_type == 'argument':
            temp[2*total_number+8] = 1
            temp_index = 2 * total_number + 6 + function_cluster + global_cluster + 2 + int(s_cluster) + 2
            temp[temp_index] = 1

    whole_list.append(temp)

if_input = pd.DataFrame(whole_list)
if_input.to_csv('if_input.csv', index=False)
