import numpy as np
import matplotlib.pyplot as plt
import random
import time
import os
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import scipy.sparse as scs # sparse matrix construction
import scipy.linalg as scl # linear algebra algorithms



print(os.listdir("/Users/YunweiDu/archive"))


data = pd.read_csv("/Users/YunweiDu/archive/small1.csv")



#np.random.seed(42)
def sudoku(snx, pro, i, j):
    en=0; en1=0
    for ro in range(9):
        if snx[i,j]==snx[ro,j]:
            en = en  + 1
        if pro==snx[ro,j]:
            en1 = en1 + 1
        if snx[i,j]==snx[i,ro]:
            en  = en  + 1
        if pro==snx[i,ro]:
            en1 = en1 + 1

    for ro in range(3):
        for co in range(3):
            if  i<3:
                x0 = 0
            elif i<6:
                x0 = 3
            else:
                x0 = 6

            if  j<3:
                y0 = 0
            elif j<6:
                y0 = 3
            else:
                y0 = 6

            if sn1[i,j]==sn1[ro+x0,co+y0]:
                en = en + 1
            if pro==sn1[ro+x0,co+y0]:
                en1 = en1 + 1
    return en, en1

corr_cnt = 0
start = time.time()
#get constraints
sn = np.zeros((9, 9))
for w in range(2):
    quiz = data["quizzes"][w]
    sn = np.reshape([int(c) for c in quiz], (9, 9))
    sn1 = sn.copy()
    sn1[sn1 == 0] = 1



    for n in range(300):#initiate temperature
        temp = 1-n/299+0.00001
        beta  = 1.0/temp
        for imetro in range(200):#times of internal circulation
            for i in range(9):
                for j in range(9):
                    if sn[i, j] != 0:
                        continue
                    en = 0;
                    en1 = 0
                    pro = random.randint(1, 9)
                    if pro == sn1[i, j]:
                        continue
                    en, en1 = sudoku(sn1, pro, i, j)

                    if (en - 3) >= en1:
                        sn1[i, j] = pro
                    elif random.random() < np.exp((en - 3 - en1) * beta):
                        sn1[i, j] = pro

    total_en = 0
    for i in range(9):
            for j in range(9):
                en, en1 =  sudoku(sn1, pro, i, j)
                total_en = total_en + en

    if total_en-3*81 > 0:
        print ('fail')
    else:

        corr_cnt += 1

    if (w + 1) % 5 == 0:
        end = time.time()
        print("Aver Time: {t:6.2f} secs. Success rate: {corr} / {all} ".format(t=(end - start) / (w + 1), corr=corr_cnt,
                                                                    all=w + 1))

end = time.time()
print("Aver Time: {t:6.2f} secs. Success rate: {corr} / {all} ".format(t=(end - start) / (w + 1), corr=corr_cnt,
                                                                       all=w + 1))
