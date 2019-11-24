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
    