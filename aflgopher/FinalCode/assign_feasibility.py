import os

def assign(file1, file2):
    '''

    :param file1: BBtable
    :param file2: distance.cfg
    :return: None
    '''
    distance = {}
    with open(file2, 'r') as r:
        for line in r.readlines():
            temp = line.split(',')
            position = temp[0].strip()
            feasibility = temp[1].strip()
            distance[position] = feasibility

    r.close()

    with open(os.environ.get('TMP_DIR')+'/BB_result.txt', 'a') as w:
        with open(os.environ.get('TMP_DIR')+'/BBtable.txt', 'r') as f:
            for line in f.readlines():
                temp = line.strip().split()
                BB_position = temp[1]
                if BB_position in distance.keys():
                    res = distance[BB_position]
                else:
                    res = '1000000'
                w.write(res)
                w.write('\n')
    w.close()
    f.close()

if __name__ == '__main__':
    assign(os.environ.get('TMP_DIR')+'/BBtable.txt', os.environ.get('TMP_DIR')+'/distance.cfg.txt')
