import timeit
import math as mt
import statistics as st
from xlrd import open_workbook,cellname
import numpy as np
import time

def ERRORS(l,ln,rows,cols):
    p=[]
    ss=0
    s=0
    count=0
    for i in range(rows):
        for j in range(cols):
            if l[i][j]!=0:
                ss+=(l[i][j]-ln[i][j])**2
                s+=l[i][j]-ln[i][j]
                count+=1
    p.append(abs(mt.sqrt(ss)/count))
    p.append(abs(s/count))
    return p


def Normalize(x,rows,cols):
    s=0
    count=0
    for i in range(cols):
        if x[i] !=99 :
            s+=x[i]
            count+=1
    av = s/count
    for i in range(cols):
        if x[i] != 99 :
            x[i] = x[i]-av
    return x

def SGD(data,rows,cols):
    

    n_factors = 10  
    alpha = .01 
    n_epochs = 10 

    
    p = np.random.normal(0, .1, (rows, n_factors))
    q = np.random.normal(0, .1, (cols, n_factors))

    
    for _ in range(n_epochs):
        for u in range(rows):
            for i in range(cols):
                if data[u][i]!=0:
                    r_ui=data[u][i]
                    err = r_ui - np.dot(p[u], q[i])    
                    p[u] += alpha * err * q[i]
                    q[i] += alpha * err * p[u]
    return p,q


def estimate(u, i):
    return np.dot(p[u], q[i])


def Predict():
    #concepts=20
    #presetting the number of concepts we desire to have in the decompositons.
    #Must be lesser than 100
    book = open_workbook('jester-data-1.xlsx')
    sheet = book.sheet_by_index(0)
    rows = sheet.nrows
    cols = sheet.ncols
    l=np.zeros((rows,cols))
    for i in range(rows):
        for j in range(cols):
            val = sheet.cell(i, j).value
            if val!=99:
                l[i][j]=1+(val+10)//5
            else:
                l[i][j]=99
    #print(l)
    for i in range(rows):
        l[i]=Normalize(l[i],rows,cols)
        
        for j in range(cols):
            if l[i][j]==99:
                l[i][j]=0
    start=time.time()
    p,q=SGD(l,rows,cols)
    end=time.time()
    print("Time taken for prediction"),
    print(end-start)
    ln=np.zeros((rows,cols))
    for i in range(rows):
        for j in range(cols):
            ln[i][j]=np.dot(p[i],q[j])
    print(ERRORS(l,ln,rows,cols))
Predict()
