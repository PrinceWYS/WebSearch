# coding: utf-8 
from difflib import restore
from distutils.filelist import FileList
from fileinput import filename
import os
import pandas as pd
import numpy as np
import invertedIndex as it
import indexCompression as ic
import synonymExpansion as se
import tokenization 
from collections import defaultdict
import math
import random
import heapq


def calculateTFAndIDF(invertedIndex):
    '''
    计算每一个文件中每一个词项的TF
    计算全部的向量
    invertedIndex:倒排索引表
    '''

    filelist = it.getFile()    #获取文件列表
    if not os.path.exists('src/hIDF.npy'): #判断是否存在IDF文件
        hIDF =  defaultdict(set)
        for key in invertedIndex:
            n =math.log((len(filelist)-1)/len(ic.restoreDocId(key,invertedIndex)),10) #计算idf
            if n>=2:
                hIDF[key]=n
        np.save('src/hIDF.npy', hIDF)
    if not os.path.exists('src/wtd.npy'):       # 推断向量是否计算好
        hIDF = np.load('src/hIDF.npy',allow_pickle=True).item()   # 读取IDF文件
        keyList = list(hIDF.keys())         # 词项列表
        totalTF = defaultdict(list)
        for i in range(len(filelist)):
            totalTF[i]=[0]*len(keyList)     # 初始化向量
        for j in range(len(keyList)):
            restoreList = ic.restoreTF(keyList[j],invertedIndex)
            for i in range(len(restoreList)):
                totalTF[restoreList[i][0]][j] = (1 + math.log(restoreList[i][1],10))*hIDF[keyList[j]] #计算权重
        vecLength = defaultdict()           # 存储向量长度
        for i in range(len(filelist)):
            sum=0
            for j in range(len(keyList)):
                if totalTF[i][j]>0:
                    sum += totalTF[i][j]*totalTF[i][j]
            vecLength[i]=math.sqrt(sum)
        np.save('src/vecLength.npy', vecLength)
        np.save('src/wtd.npy', totalTF)
        
    
def clusterPruning():

    '''
    选择100个文档作为先导者
    计算每一个文档跟随的先导者并存储
    invertedIndex:倒排索引表
    '''
    vecLength=np.load('src/vecLength.npy',allow_pickle=True).item()    # 读取向量长度
    filelist = it.getFile()                      # 获取文件列表
    wtd = np.load('src/wtd.npy',allow_pickle=True).item()
    num = random.sample(range(1, len(filelist)-1), 100) # 随机取100个文档作为先导者
    num.sort()
    pioneer = defaultdict(list)


    for i in range(1,101,1):
        pioneer[num[i-1]]=[]

    for i in range(1,len(filelist),1):     # 遍历文档集寻找与每个文档最接近的先导者
        temp =defaultdict(list)
        heap = []                          # 堆结构存储向量相似度
        for j in range(len(num)):
            res = vectorCal(wtd[i],wtd[num[j]],vecLength[i],vecLength[num[j]]) # 计算相似度
            if res in temp:
                temp[res].append(j)
            else:
                temp[res]=[j]
            heapq.heappush(heap,-res)                                          # 压入堆中
        for k in range(4):            
            top = -heapq.heappop(heap)                                             # 获取堆顶部的最大值 
            pioneer[num[temp[top].pop()]].append(i)                                # 放入最接近的先导者中
    np.save('src/pioneer.npy', pioneer)                                            # 存储先导者文件                                     # 存储追随者文件


def vectorCal(vecA,vecB,lengthA,lengthB):
    sum =0
    for i in range(len(vecA)):
        sum+=vecA[i]*vecB[i]
    if lengthA==0 or lengthB ==0:
        return 0
    else:
        return sum/(lengthA*lengthB)

def getRes(queryVec,wtd,vecLength):
    query = queryVec[0]
    fileList = it.getFile()
    # vecLength=np.load('src/vecLength.npy',allow_pickle=True).item()
    pioneer=np.load('src/pioneer.npy',allow_pickle=True).item()
    pioList = list(pioneer.keys())
    Candidate=[]
    heap=[]
    temp =defaultdict(list)
    for key in pioList:
        res = vectorCal(wtd[key],query,vecLength[key],queryVec[1])
        if res in temp:
            temp[res].append(key)
        else:
            temp[res]=[key]
        heapq.heappush(heap,-res)
    for i in range(5):
        top = -heapq.heappop(heap)
        Candidate.append(temp[top].pop())
    heap =[]
    index =defaultdict(list)
    out = []
    for i in range(5):
        for key in pioneer[Candidate[i]]:
            res = vectorCal(wtd[key],query,vecLength[key],queryVec[1])
            if res in index:
                index[res].append(key)
            else :
                index[res] =[key]
            heapq.heappush(heap,-res)
    for i in range(10):
        top = -heapq.heappop(heap)
        if top ==0:
            return out     
        out.append(fileList[index[top].pop()])
    out = set(out)
    out = list(out)
    return out


def getQueryVec(queryStr, vecLength = None, hIDF = None):
    if vecLength is None:
        vecLength=np.load('src/vecLength.npy',allow_pickle=True).item()
    words =tokenization.tokenize(queryStr)
    if hIDF is None:
        hIDF = np.load('src/hIDF.npy',allow_pickle=True).item()
    keyList = list(hIDF.keys())
    res=[0]*len(keyList)
    sum=0
    for i in range(len(keyList)):
        tf=0
        seList = se.getSyn(keyList[i])
        for key in seList:
            tf+= words.count(key)
        
        if tf > 0:
            res[i] = (1+math.log(tf,10)*hIDF[keyList[i]])
            sum += res[i]*res[i]
    queLength = math.sqrt(sum)

    return [res,queLength]


def topSort(nameList,query, wtd, vecLength):
    # wtd = np.load('src/wtd.npy',allow_pickle=True).item()
    # vecLength=np.load('src/vecLength.npy',allow_pickle=True).item()
    queryVec =query[0]
    res=[]
    temp =defaultdict(list)
    heap =[]
    for key in nameList:
        max = vectorCal(wtd[key],queryVec,vecLength[key],query[1])
        heapq.heappush(heap,-max)
        if max in temp:
            temp[max].append(key)
        else:
            temp[max]=[key]

    score = []
    for i in range(len(nameList)):
        top = -heapq.heappop(heap)
        # # 过滤掉相似度为0的文件
        # if top == 0:
        #     return res, score

        res.append(temp[top].pop())
        score.append(top)

    return res,score
    


