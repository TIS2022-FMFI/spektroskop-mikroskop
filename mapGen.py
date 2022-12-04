import random as rnd

with open("test.txt", "w") as sxbao:
    for j in range(50):
        for k in range(50):
            if k == 0:
                line = str(rnd.randrange(0, 14))
                continue
            line += ' ' + str(rnd.randrange(0, 14))
        sxbao.write(line+'\n')
