import random as rnd

with open("test.txt", "w") as f:
    for i in range(500):
        if i == 0:
            line = str(i)
            continue
        line += ',' + str(i)
    f.write(line+'\n')
    for j in range(500):
        for k in range(500):
            if k == 0:
                line = str(rnd.randrange(0, 200))
                continue
            line += ',' + str(rnd.randrange(0, 200))
        f.write(line+'\n')
