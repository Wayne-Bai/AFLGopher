import os
import argparse
import pandas


def get_filelist(path):

    Filelist = []

    for home, dirs, files in os.walk(path):
        for filename in files:
            Filelist.append(os.path.join(home, filename))

    c_file_list = [fn for fn in Filelist if fn.endswith('.c')]

    return c_file_list

if __name__ =="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--file", default=None)
    args = parser.parse_args()

    # path ='../libxml2'
    path = args.file

    c_file_list = get_filelist(path)

    # print(len(c_file_list))
    # print(c_file_list)
    with open('if_source_position.txt', 'a') as w:
        for i in c_file_list:
            print(i)
            # if 'buf.c' in i:
            count = 0
            with open(i, 'r', encoding = "ISO-8859-1") as f:
                # file_name = i.strip().split('/')[-1]
                for line in f.readlines():
                    count += 1
                    if 'if ' in line and '#' not in line and '/' not in line and '\\' not in line and line.strip()[0] != '*':
                        w.write(i)
                        w.write('    ')
                        w.write(str(count))
                        w.write('\n')
            f.close()
    w.close()
