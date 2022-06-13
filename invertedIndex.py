# coding: utf-8 
import os
from collections import defaultdict
import re
import sys
import tokenization as tk

def scanFiles():
    '''
    扫描path下的所有文件,返回文件名列表
    return : 文件名列表
    '''
    curPath =  os.path.abspath(os.path.dirname(__file__))  # 当前目录
    path = os.path.join(curPath, 'Reuters')  # 文件路径
    for root, dirs, files in os.walk(path):
        return files
        
def getFile():
    file = scanFiles()
    fileId = [0]
    for i in range(len(file)):
        fileId.append(int(file[i].split('.')[0]))
    fileId.sort()
    # for i in range(1,len(file)+1,1):
    #     fileId[i] = str(fileId[i])+'.html'
    return fileId



def createInvertedIndex():

    fileList = getFile()  # 扫描文件夹下的所有文件
    ''''
    创建倒排索引
    fileList : 文件列表
    path : 文件所在路径
    return : 倒排索引(defaultdict(list)类型)
    '''
    invertedIndex = defaultdict(list)
    if fileList:  # 文件列表非空
        for i in range(1,len(fileList),1):
            #fileDir = os.sep.join([filePath, fileName])
            pos = 0
            f = open('Reuters/'+str(fileList[i])+'.html', 'r', encoding='unicode_escape')
            for line in f:
                # for word in re.split(r'[^0-9a-zA-Z]\s*', line):  # 以分隔词项
                for word in tk.tokenize(line):
                    if len(word) == 0:
                        continue
                    word = word.lower()  # 不区分大小写)
                    if word in invertedIndex:
                        invertedIndex[word].append(i)
                        invertedIndex[word].append(pos)
                    else:
                        invertedIndex[word] = list([i,pos])
                    pos+=1
                    
    # 将文件按照名称进行排序 并且添加TF值
    ret = defaultdict(set)
    for key in invertedIndex:
        ret[key] = invertedIndex[key]
        temp = []
        index = []
        j = 1
        for i in range(0,len(ret[key]),2):
            index.append(ret[key][i+1])
            if i == len(ret[key])-2 or ret[key][i] != ret[key][i+2]:
                temp.append(ret[key][i])
                temp.append(j)
                temp.append(index)
                index =[]
                j = 1
            else:
                j = j +1

        ret[key] = temp
                 

    return ret


