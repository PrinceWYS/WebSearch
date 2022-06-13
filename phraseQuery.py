import os
from collections import defaultdict
import pandas as pd
import re
import indexCompression as ic
import invertedIndex as it
import tokenization as tk



class termPosIndex:
    '''
    单一词项的位置信息索引
    term : 词项
    docNum : 文档数
    posList : 位置信息索引
    '''
    term = None
    docNum = 0
    posList = defaultdict(list)

    def __init__(self, term = None, docNum=0, posList=None):
        self.term = term
        self.docNum = docNum
        if posList is not None:
            self.posList = posList

    def addDoc(self,oneItem):
        self.docNum += 1
        docName = oneItem[0]
        posList = oneItem[1]
        if docName in self.posList:
            self.posList[docName].extend(posList)
        else:
            self.posList[docName] = posList



class PositionIndex:
    '''
    所有词项的位置信息索引
    posIndex : 词项字典 (term : termPosIndex)
    '''

    posIndex = defaultdict(termPosIndex)  # 以词项为key，termPosIndex为value

    def __init__(self, posIndex = None):
        if posIndex != None:
            self.posIndex = posIndex
    

    # 为词项添加位置信息索引
    def addTerm(self, term, docName, posList):
        if term in self.posIndex:
            self.posIndex[term].docNum += 1
            self.posIndex[term].posList[docName] = posList
        else:
            self.posIndex[term] = termPosIndex(term, 1, {docName: posList})



def scanFiles(path):
    '''
    扫描path下的所有文件,返回文件名列表
    path : 文件夹路径
    return : 文件名列表
    '''
    for root, dirs, files in os.walk(path):
        return files


def writeFilePosIndex(posIndex,fileName = 'src/posIndex.txt'):
    '''
    将位置索引写入到文件中
    posIndex : PositionIndex类
    '''
    curPath = os.path.abspath(os.path.dirname(__file__))
    fileName = os.path.join(curPath, fileName)
    f = open(fileName, 'w', encoding='utf-8')
    for term in posIndex.posIndex:
        f.write('['+term + ' ' + str(posIndex.posIndex[term].docNum) + ' ')
        for docName in posIndex.posIndex[term].posList:
            f.write('{'+str(docName) + ':')
            flag = True
            for pos in posIndex.posIndex[term].posList[docName]:
                if flag :
                    f.write(str(pos))
                    flag = False
                else:
                    f.write(','+str(pos))
            f.write('}')
        f.write(']\n')
    f.close()


def readFilePosIndex():
    '''
    读取位置索引文件
    return : PosisiontIndex类的实例
    '''
    curPath = os.path.abspath(os.path.dirname(__file__))
    fileName = 'posIndex.txt'
    fileName = os.path.join(curPath, 'src',fileName)
    f = open(fileName, 'r', encoding='utf-8')
    myPosIndex = PositionIndex()

    for line in f:
        line = line.strip() #去掉前后空格
        if line[0] == '[' :
            line = line[1:-1]
            term, docNum, posList = line.split(' ')
            posList = posList.split('{')

            for i in range(1, len(posList)):
                docName, posList[i] = posList[i].split(':')
                posList[i] = posList[i].strip('}') # 删除最后的}
                posList[i] = [int(pos) for pos in posList[i].split(',')]

                if term in myPosIndex.posIndex:
                    myPosIndex.posIndex[term].addDoc([int(docName), posList[i]])
                else:
                    myPosIndex.posIndex[term] = termPosIndex(term, int(docNum), {int(docName): posList[i]})
                
    f.close()
    return myPosIndex


def createPoistionIndex():
    '''
    创建位置索引
    fileList : 文件列表
    return : 所有词项的位置信息索引 (PositionIndex)
    '''
    curPath = os.path.abspath(os.path.dirname(__file__))  # 当前目录
    filePath = os.path.join(curPath, 'Reuters')  # 文件路径
    fileList = scanFiles(filePath)  # 扫描文件夹下的所有文件

    finalPosIndex = PositionIndex()
    for fileName in fileList:
        fileDir = os.sep.join([filePath,fileName])
        f = open(fileDir, 'r', encoding='unicode_escape')
            
        tempDict = defaultdict(list)
        pos = 0
        for line in f:
            # for word in re.split(r'[^0-9a-zA-Z]\s*', line):  # 以分隔词项
            for word in tk.tokenize(line):
                if len(word) == 0: # 空字符
                    continue
                word = word.lower()  # 不区分大小写

                if word in tempDict:
                    tempDict[word].append(pos)
                else:
                    tempDict[word] = [pos]
                pos += 1

        fileName = int(fileName.split('.')[0])  # 去掉后缀
        for key in tempDict:
            finalPosIndex.addTerm(key, fileName, tempDict[key])
                
    writeFilePosIndex(finalPosIndex)
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


def restorePosIndex(invertedIndex):
    '''
    恢复位置索引
    invertedIndex : 倒排索引
    return : 恢复后的位置索引
    '''
    if not os.path.exists('src/posIndex.txt'):  # 如果不存在了位置信息索引
        PosIndex = PositionIndex()
        # docNameList = it.getFile()
        for term in invertedIndex.keys():
            totalList = ic.restoreIndex(term,invertedIndex)
            docNum = len(totalList)  # 获取文件个数
            docList = defaultdict(list) 
            for oneList in totalList:
                docName = oneList[0]  # 获取文件序号
                # docName = docNameList[oneList[0]]  # 获取文件名称

                tempList = oneList.copy()
                del(tempList[0])  # 删除第一个元素，即删除doc序号
                for pos in tempList:
                    docList[docName].append(pos)
            
            if term in PosIndex.posIndex:
                PosIndex.posIndex[term].addDoc([docName,docList])
            else:
                PosIndex.posIndex[term] = termPosIndex(term, docNum, docList)

        writeFilePosIndex(PosIndex)  # 写入到文件中
    else:
        return readFilePosIndex()  # 直接从文件中读取

    return PosIndex


def phraseQuery(termList,positionIndex):
    '''
    进行短语查询
    termList : 查询的短语
    posIndex : 位置索引
    return : 包含短语的文档列表
    '''

    # positionIndex = restorePosIndex(invertedIndex)

    docList = []
    preTerm = None
    for term in termList:
        if term in positionIndex.posIndex:
            # 先获取当前term的doc信息
            curDocList = []
            for doc in positionIndex.posIndex[term].posList:
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
    
    docList.sort()  # 对文件名进行排序

    return docList


