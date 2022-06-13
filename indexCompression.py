# coding: utf-8 
import os
from collections import defaultdict
import re
import sys
import numpy as np
from numpy import uint8
import pandas as pd 



def compressionIndex(invertedIndex):
    '''
    索引压缩与存储
    invertedIndex : 原始倒排索引
    '''
    docIdDef = defaultdict(set) 
    VB_encode = defaultdict(set)

    for key in invertedIndex:
        temp = invertedIndex[key]
        for i in range(len(temp)-3,-1,-3):
            if i!=0:
                temp[i] = temp[i]-temp[i-3]
            for j in range(len(temp[i+2])-1,0,-1):
                temp[i+2][j] = temp[i+2][j]-temp[i+2][j-1]

        docIdDef[key] = temp


    for key in docIdDef:
        VB_encode[key] = []
        for i in range(len(docIdDef[key])):
            if i%3 !=2:
                j = docIdDef[key][i]
                k = 1
                while j >= k * 128:
                    k = k * 128
                while k > 1:
                    VB_encode[key].append(uint8(j//k))
                    j = j%k
                    k = k//128
                VB_encode[key].append(uint8(j+128))
            else:
                for n in range(len(docIdDef[key][i])):
                    k =1
                    j =docIdDef[key][i][n]
                    while j >= k * 128:
                        k = k * 128
                    while k > 1:
                        VB_encode[key].append(uint8(j//k))
                        j = j%k
                        k = k//128
                    VB_encode[key].append(uint8(j+128))
                    




    np.save('src/invertIndexFile.npy', VB_encode) 
    


def restoreDocId(key,VB_encode):
    '''
    索引还原
    invertedIndex : 压缩倒排索引
    key : 想要还原的关键字
    return : 还原后的索引
    '''
    defId = 0 #计算docID
    temp = []
    j=0
    k = 0
    for i in range(len(VB_encode[key])):
        if VB_encode[key][i] < 128:
            k = k*128 + VB_encode[key][i] 
        else:
            if j == 0:
                k = k *128 + VB_encode[key][i] -128
                defId += k
                temp.append(defId)
                k=0
                j=1
            else:
                if j==1:
                    k = k *128 + VB_encode[key][i] -128
                    j=1+k
                    k=0
                else:
                    k=0
                    if j==2:
                        j=0
                    else :
                        j=j-1

    return temp

def restoreTF(key,VB_encode):
    '''
    索引还原
    invertedIndex : 压缩后的倒排索引
    key : 想要还原的关键字对应的倒排索引
    return : 还原后的索引和TF值
    '''
    defId = 0 #计算docID
    ret = []
    j=0
    k = 0
    for i in range(len(VB_encode[key])):
        if VB_encode[key][i] < 128:
            k = k*128 + VB_encode[key][i] 
        else:
            if j == 0:
                temp =[]
                k = k *128 + VB_encode[key][i] -128
                defId += k
                temp.append(defId)
                k=0
                j=1
            else:
                if j==1:
                    k = k *128 + VB_encode[key][i] -128
                    temp.append(k)
                    ret.append(temp)
                    j=1+k
                    k=0
                else:
                    k=0
                    if j==2:
                        j=0
                    else :
                        j=j-1

    return ret

def restoreIndex(key,VB_encode):
    '''
    索引还原
    invertedIndex : 压缩倒排索引
    key : 想要还原的关键字
    return : 还原后的索引
    '''
    defId = 0 #计算docID
    defIndex =0
    temp = []
    j=0
    k = 0
    for i in range(len(VB_encode[key])):
        if VB_encode[key][i] < 128:
            k = k*128 + VB_encode[key][i] 
        else:
            if j == 0:
                k = k *128 + VB_encode[key][i] -128
                defId += k
                temp.append(defId)
                k=0
                j=1
            else:
                if j==1:
                    k = k *128 + VB_encode[key][i] -128
                    temp.append(k)
                    j=1+k
                    k=0
                else:
                    k = k *128 + VB_encode[key][i] -128
                    defIndex+=k
                    temp.append(defIndex)
                    k=0
                    if j==2:
                        defIndex=0
                        j=0
                    else :
                        j=j-1
    ret = []
    k=0
    size=0
    for i in range(len(temp)):
        if k==0:
            doc=[temp[i]]
            k=1
        else:
            if k==1:
                size=temp[i]
                k=2
            else:
                doc.append(temp[i])
                size=size-1
                if size==0:
                    ret.append(doc)
                    k=0



    return ret