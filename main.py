# coding: utf-8 
import invertedIndex as it
import indexCompression as ic
import vectorSpaceModel as vsm
import numpy as np
import os
import BTree
import boolSearch
import phraseQuery
import browseHtml
import time

fileList = []



def main():
    #invertedIndex = it.createInvertedIndex()
    print('\033[32m#'*27+'使用简介'+'#'*27+'\033[0m')
    print('输入1,使用普通查询')
    print('输入2,使用topK查询')
    print('输入3,开/关向量排序')
    print('输入4,退出程序')
    print('\033[32m#'*62+'\033[0m')
    print()

    print('初始化引擎中....')
    # global fileList
    # fileList = it.getFile()                       # 扫描文件夹下的所有文件
    if not os.path.exists('src/invertIndexFile.npy'): # 扫描是否存在倒排索引表
        startTime = time.time()
        invertedIndex = it.createInvertedIndex()  # 创建倒排索引和词典
        endTime = time.time()
        print('创建倒排索引和词典完成，用时：%ds' % (endTime - startTime))

        startTime = time.time()
        ic.compressionIndex(invertedIndex) #索引压缩与存储倒排索引表
        endTime = time.time()
        print('索引压缩完成，用时：%ds' % (endTime - startTime))


    invertIndex = np.load('src/invertIndexFile.npy', allow_pickle=True).item() #从文件中读取倒排索引表22
    if not os.path.exists('src/hIDF.npy'):
        vsm.calculateTFAndIDF(invertIndex)               # 计算tf值和idf
    if not os.path.exists('src/pioneer.npy'):
        vsm.clusterPruning()                             # 簇剪枝
    PosIndex = phraseQuery.restorePosIndex(invertIndex)  # 从倒排索引表中恢复位置信息

    #vsm.clusterPruning()
    BTree.buildTree(invertIndex)

    wtd = np.load('src/wtd.npy',allow_pickle=True).item()
    vecLength=np.load('src/vecLength.npy',allow_pickle=True).item()

    topK = False

    while(True):
        choose = input('\n请选择使用的查询模式：')
        if choose == '1':
            word = input("请输入要查询的词项:\n")
            startTime = time.time()
            res = boolSearch.Bool(word, invertIndex, PosIndex)
            if topK==True:
                queryVec =vsm.getQueryVec(word,vecLength)
                res,score =vsm.topSort(res,queryVec,wtd,vecLength)
            # wordList = word.split()
            # res = phraseQuery.phraseQuery(wordList, phraseQuery.createPoistionIndex())
            docNameList = it.getFile()
            nameList = []
            # print(res)
            for r in res:
                # print(docNameList[r])
                nameList.append(docNameList[r])
            endTime = time.time()
            if topK==True:
                browseHtml.openHtml(nameList,endTime-startTime,score)
            else:
                browseHtml.openHtml(nameList,endTime-startTime)
            continue
        elif choose == '2':
            word = input("请输入要查询的词项:\n")
            startTime = time.time()
            queryVec =vsm.getQueryVec(word,vecLength)
            nameList = vsm.getRes(queryVec,wtd,vecLength)
            endTime = time.time()
        elif choose == '3':
            if topK==False:
                topK = True
                print('打开topK排序')
                continue
            else:
                topK = False
                print('关闭topK排序')
                continue
        elif choose == '4':
            break

        browseHtml.openHtml(nameList, endTime-startTime)  # 浏览器展示

    
    # lis = ic.restoreIndTF('input',invertIndex)
    # vsm.calculateTFAndIDF(invertIndex)

    # print("Welcome to our information retrieval system:\n")
    # while 1:
    #     print("Please enter what you want to retrieve and press Enter to end:")
    #     reqStr = input()


    #     print("Retrieved results:\n")
main()