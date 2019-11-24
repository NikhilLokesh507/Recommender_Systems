import timeit
import math as mt
import statistics as st
from xlrd import open_workbook,cellname
import numpy as np
from scipy import stats as sp
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
                s+=abs(l[i][j]-ln[i][j])
                count+=1
    p.append(abs(mt.sqrt(ss)/count))
    p.append(abs(s/count))
    return p
def PearsonCorr(x,y):
    avx=np.average(x)
    avy=np.average(y)
    x-=avx
    y-=avy
    u=np.dot(x,y.T)
    x=x**2
    y=y**2
    s=u[0]
    s1=np.sum(x)
    s2=np.sum(y)
    return s/mt.sqrt(s1*s2)

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


def AvRating(l,rows,cols):
    s=0
    c=0
    for i in range(rows):
        for j in range(cols):
            if l[i][j]!=0:
                s+=l[i][j]
                c+=1
    return s/c

def AvUserRating(user,cols):
    s=0
    c=0
    for j in range(cols):
        if user[j]!=0:
            s+=user[j]
            c+=1
    return s/c

def AvMovieRating(movie,rows):
    s=0
    c=0
    for i in range(rows):
        if movie[i]!=0:
            s+=movie[i]
            c+=1
    return s/c

def TotalAv(l,rows,cols):
    s=0
    c=0
    for i in range(rows):
        for j in range(cols):
            if l[i][j]>0:
                s+=l[i][j]
                c+=1
    return s/c
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
    sim=np.zeros((cols,cols))
    for i in range(cols):
        for j in range(i+1,cols):
            x=l[:,i:i+1].T
            y=l[:,j:j+1].T
            sim[i][j]=PearsonCorr(x,y)
            sim[j][i]=sim[i][j]
    ln=np.zeros((rows,cols))
    lp=np.zeros((rows,cols))
    m=AvRating(l,rows,cols)
    sumsim=np.sum(sim)
    

    #start without baseline
    start=time.time()
    for i in range(rows):
        for j in range(cols):
            s=0
            for k in range(cols):
                if l[i][k]!=0:
                    s+=sim[j][k]*l[i][k]
            ln[i][j]=s/sumsim
    end=time.time()
    print("time for predicitng svd without baseline: "),
    print(end-start)
    print(ERRORS(l,ln,rows,cols))
    

    #here we start with baseline
    '''movieavs=[AvMovieRating(l[:,j:j+1],rows) for j in range(cols)]
    useravs=[AvUserRating(l[i],cols) for i in range(rows)]
    av=TotalAv(l,rows,cols)
    start=time.time()
    for i in range(rows):
        print(i)
        for j in range(cols):
            s=0
            for k in range(cols):
                s+=sim[j][k]*(l[i][k]-(av+movieavs[k]+useravs[i]))
            lp[i][j]=s/sumsim
    end=time.time()
    print("time for predicitng svd with baseline: "),
    print(end-start)
    print(ERRORS(l,lp,rows,cols))'''

Predict()
