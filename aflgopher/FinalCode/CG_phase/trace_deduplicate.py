with open("Copy of Cnames.txt", 'r') as f:
    with open('func name.txt', 'a') as w:
        temp = []
        for line in f.readlines():
            if line not in temp:
                w.write(line)
                temp.append(line)

f.close()
w.close()
