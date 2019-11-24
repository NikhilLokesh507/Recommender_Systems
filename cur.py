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

def ERRORSw(l,ln,rows,cols):
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
    p.append(abs(mt.sqrt(ss)/count)/1e+04)
    p.append(abs(s/count)/1e+04)
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
    ls=np.square(l)
    item=np.zeros((cols))
    user=np.zeros((rows))
    np.sum(ls,axis=0,out=item)
    np.sum(ls,axis=1,out=user)
    f=np.sum(ls)
    #print(f)
    item=np.true_divide(item,f)
    user=np.true_divide(user,f)
    x=[]
    y=[]
    rank=20
    count=0
    while count < rank :
        r=np.random.choice(range(0,cols),p=item)
        if r not in y:
            count+=1
            y.append(r)
    count=0
    while count < rank :
        r=np.random.choice(range(0,rows),p=user)
        if r not in x:
            count+=1
            x.append(r)
    x.sort()
    y.sort()
    C=np.zeros((rows,rank))
    for j in range(rank):
        col=y[j]
        div=mt.sqrt(item[j]*rank)
        C[:,j:j+1]=np.true_divide(l[:,col:col+1],div)
    R=np.zeros((rank,cols))
    for i in range(rank):
        row=x[i]
        div=mt.sqrt(user[i]*rank)
        R[i:i+1,:]=np.true_divide(l[row:row+1,:],div)
    W=np.zeros((rank,rank))
    for i in range(rank):
        for j in range(rank):
            W[i][j]=l[x[i]][y[j]]
    x, s, y = np.linalg.svd(W)
    sn=np.power(s,2)
    sn=np.power(sn,-1)
    sn=np.diag(sn)
    U=np.matmul(np.matmul(y.T,sn),x.T)
    el=np.matmul(np.matmul(C,U),R)
    print(ERRORSw(l,el,rows,cols))

    #this is for 90% energy calculation
    '''s1=[]
    suml=0
    c=0
    sums=sum(sn)
    for h in sn:
        suml+=h
        c+=1
        s1.append(h)
        if suml>0.9*sums:
            break
    x=x[:,:c]
    y=y[:c,:]
    sn=s1
    sn=np.power(sn,-1)
    sn=np.diag(sn)
    U=np.matmul(np.matmul(y.T,sn),x.T)
    el=np.matmul(np.matmul(C,U),R)
    print(ERRORS(l,el,rows,cols))
    #90 percent energy prediction concludes
    '''


start=time.time()
Predict()
end=time.time()
print(end-start)
