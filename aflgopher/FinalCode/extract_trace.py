import os
def extract(file_name, BB_dic, CG_dic):

    file_number = file_name.split('/')[-1]
    
    with open(file_name, 'r') as f:
        os.mkdir(os.environ.get('IP_DIR')+'/BB/'+ file_number)
        with open(os.environ.get('IP_DIR')+'/BB/'+ file_number + '/trace', 'a') as BB:
            with open(os.environ.get('IP_DIR')+'/CG/'+ file_number + '-CG', 'a') as CG:
                for line in f.readlines():
                    if '----' not in line:
                        temp = line.split()
                        if temp[0] == 'cg':
                            CG.write(CG_dic[int(temp[1])])
                            CG.write('\n')
                        else:
                            BB.write(BB_dic[int(temp[1])])
                            BB.write('\n')
    pass

def load2dic(file_name):

    dic = {}
    with open(file_name, 'r') as f:
        for line in f.readlines():
            if '----' not in line:
                temp = line.strip().split(' ', 1)
                dic[int(temp[0])] = temp[1]
    f.close()

    return dic

if __name__ == '__main__':

    BB_dic = load2dic(os.environ.get('TMP_DIR')+'/BBtable.txt')
    CG_dic = load2dic(os.environ.get('TMP_DIR')+'/CGtable.txt')

    for i in os.listdir(os.environ.get('IP_DIR')+'/update'):
    	try:
    	    int(i)
    	    extract(os.environ.get('IP_DIR')+'/update/'+i, BB_dic, CG_dic)
    	except:
    	    pass

