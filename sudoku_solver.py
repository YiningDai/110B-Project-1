import numpy as np
import matplotlib.pyplot as plt
import random
import time
import os
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import scipy.sparse as scs # sparse matrix construction
import scipy.linalg as scl # linear algebra algorithms
import scipy.optimize as sco # for minimization use
from scipy.optimize import minimize
import cvxpy as cvx
import math



print(os.listdir("C:/Users/Administrator/Desktop/YunweiDu/archive"))


data = pd.read_csv("C:/Users/Administrator/Desktop/YunweiDu/archive")


def fixed_constraints(N=9):
    rowC = np.zeros (N)
    rowC[0] = 1
    rowR = np.zeros (N)
    rowR[0] = 1
    row = scl.toeplitz (rowC, rowR)
    ROW = np.kron (row, np.kron (np.ones ((1, N)), np.eye (N)))

    colR = np.kron (np.ones ((1, N)), rowC)
    col = scl.toeplitz (rowC, colR)
    COL = np.kron (col, np.eye (N))

    M = int (np.sqrt (N))
    boxC = np.zeros (M)
    boxC[0] = 1
    boxR = np.kron (np.ones ((1, M)), boxC)
    box = scl.toeplitz (boxC, boxR)
    box = np.kron (np.eye (M), box)
    BOX = np.kron (box, np.block ([np.eye (N), np.eye (N), np.eye (N)]))

    cell = np.eye (N ** 2)
    CELL = np.kron (cell, np.ones ((1, N)))

    return scs.csr_matrix (np.block ([[ROW], [COL], [BOX], [CELL]]))


# For the constraint from clues, we extract the nonzeros from the quiz string.
def clue_constraint(input_quiz, N=9):
    m = np.reshape ([int (c) for c in input_quiz], (N, N))
    r, c = np.where (m.T)
    v = np.array ([m[c[d], r[d]] for d in range (len (r))])

    table = N * c + r
    table = np.block ([[table], [v - 1]])

    # it is faster to use lil_matrix when changing the sparse structure.
    CLUE = scs.lil_matrix ((len (table.T), N ** 3))
    for i in range (len (table.T)):
        CLUE[i, table[0, i] * N + table[1, i]] = 1
    # change back to csr_matrix.
    CLUE = CLUE.tocsr ()

    return CLUE
def calc_ent(x):
    ent=np.sum(np.dot(x,np.log2(x)))

    return ent



corr_cnt = 0
start = time.time()

for w in range(len(data)):
    quiz = data["quizzes"][w]

    A0 = fixed_constraints ()
    # get the constraint matrix from clue.
    A1 = clue_constraint (quiz)

    # Formulate the matrix A and vector B (B is all ones).
    A = scs.vstack ((A0, A1))
    B = np.ones ((np.size (A, 0)))


    x0=np.ones((np.size (A, 1)))
    fun=lambda x:calc_ent(x)
    con = ({'type': 'eq', 'fun': lambda x: A * x - B})
    res=minimize(fun,x0,method='SLSQP',constraints=con)
    sol=res.x


    corr_cnt += 1



end = time.time()
print("Aver Time: {t:6.2f} secs. Success rate: {corr} / {all} ".format(t=(end - start) / (w + 1), corr=corr_cnt,
                                                                       all=w + 1))
