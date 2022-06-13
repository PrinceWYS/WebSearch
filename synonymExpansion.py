# coding=UTF-8
from nltk.corpus import wordnet as wn
import os
from collections import defaultdict
from phraseQuery import PositionIndex,readFilePosIndex,writeFilePosIndex,restorePosIndex
import re
import tokenization as tk


def scanFiles(path):
    '''
    扫描path下的所有文件,返回文件名列表
    path : 文件夹路径
    return : 文件名列表
    '''
    for root, dirs, files in os.walk(path):
        return files



def createSynonymPositionIndex():
    '''
    创建位置索引
    fileList : 文件列表
    return : 所有词项的位置信息索引 (PositionIndex)
    '''

    curPath = os.path.abspath(os.path.dirname(__file__))  # 当前目录
    filePath = os.path.join(curPath, 'Reuters')  # 文件路径
    fileList = scanFiles(filePath)  # 扫描文件夹下的所有文件

    finalPosIndex = PositionIndex()
    
    count = 0
    for fileName in fileList:
        fileDir = os.sep.join([filePath,fileName])
        f = open(fileDir, 'r', encoding='unicode_escape')
            
        tempDict = defaultdict(list)  # key为词项，value为位置信息索引列表
        pos = 0
        for line in f:
        #     for word in re.split(r'[;,\s]\s*', line):
            # for word in re.split(r'[^0-9a-zA-Z]\s*', line):
            for word in tk.tokenize(line):
                if len(word) == 0:
                    continue
                word = word.lower()  # 不区分大小写

                # 将自身的值放入字典中
                if word in tempDict:
                    if pos not in tempDict[word]:
                        tempDict[word].append(pos)
                else:
                    tempDict[word] = [pos]
                    
                # 进行同义词扩展
                syns = wn.synsets(word)  # 获得所有的同义词集

                for syn in syns:  # 对于每一个同义词集
                    for lemma in syn.lemmas():  # 遍历所有的同义词
                        if lemma.name() in tempDict:
                            if pos not in tempDict[lemma.name()]:
                                tempDict[lemma.name()].append(pos)
                        else:
                            tempDict[lemma.name()] = [pos]
                
        fileName = int(fileName.split('.')[0]) # 去掉文件名的后缀
        for key in tempDict:
            finalPosIndex.addTerm(key, fileName, tempDict[key])

    writeFilePosIndex(finalPosIndex, 'synonymPositionIndex.txt')
    return finalPosIndex


def posMatch(prePosList, curPosList):
    '''
    判断两个位置列表是否匹配
    prePosList : 前一个位置列表
    curPosList : 当前位置列表
    return : True or False
    '''
    for pos in prePosList:
        if pos+1 in curPosList:
            return True
    return False


def synonymPhraseQuery(termList, positionIndex):
    '''
    同义词查询
    phraseList : 输入的短语列表
    myPosIndex : 同义词扩展后的位置索引
    return : 查询结果列表
    '''

    # positionIndex = restorePosIndex(invertedIndex)  # 从倒排索引中恢复出位置信息索引 

    docList = []
    preTerm = None
    for term in termList:
        if term in positionIndex.posIndex:
            # 先获取当前term的doc信息
            curDocList = []
            for doc in positionIndex.posIndex[term].posList:
                curDocList.append(doc)

            # 获取term同义词的doc信息
            synList = wn.synsets(term)
            for syn in synList:
                for lemma in syn.lemmas():
                    for doc in positionIndex.posIndex[lemma.name()].posList:
                        if doc not in curDocList:
                            curDocList.append(doc)

            # 与前一个term的doc取交集
            if len(docList) == 0:
                docList = curDocList
            docList = [i for i in docList if i in curDocList]
            if len(docList) == 0: # 交集为空
                return []
            
            # 判断剩余的doc中posIndex是否与前一个term的posIndex匹配
            if preTerm is None:
                preTerm = term
                continue
                
            tempDocList = docList.copy()
            for doc in tempDocList:
                if doc not in positionIndex.posIndex[term].posList:
                    docList.remove(doc)
                    continue
                if doc not in positionIndex.posIndex[preTerm].posList:
                    docList.remove(doc)
                    continue
                if posMatch(positionIndex.posIndex[preTerm].posList[doc], positionIndex.posIndex[term].posList[doc]):
                    continue
                else:
                    docList.remove(doc)
            preTerm = term

        else:  # 如果某个短语不在索引中，则返回空列表
            return []
    
    docList.sort()  # 按照文件名称排序
    return docList 


def getSyn(term):
    '''
    term : 一个单词
    return : 返回同义词列表
    '''
    retList = []
    synList = wn.synsets(term)
    for syn in synList:
        for lemma in syn.lemmas():
            if lemma.name() not in retList:
                retList.append(lemma.name())

    return retList