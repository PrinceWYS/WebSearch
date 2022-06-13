import numpy as np

def string_distance(str1, str2):
    '''
    计算两个字符串的编辑距离
    :param str1: 第一个字符串
    :param str2: 第二个字符串
    :return: 编辑距离
    '''
    m = str1.__len__()
    n = str2.__len__()
    distance = np.zeros((m+1, n+1))
 
    for i in range(0, m+1):
        distance[i, 0] = i
    for i in range(0, n+1):
        distance[0, i] = i
 
    for i in range(1, m+1):
        for j in range(1, n+1):
            if str1[i-1] == str2[j-1]:
                cost = 0
            else:
                cost = 1
            distance[i, j] = min(distance[i-1, j]+1, distance[i, j-1]+1, distance[i-1, j-1]+cost)  # 分别对应删除、插入和替换
 
    return distance[m, n]

def findMin(word, invertedIndex):
    '''
    找出距离拼写错误的词编辑距离最近的单词集合
    :param word: 给出的单词
    :param invertedIndex: 倒排索引表
    :return: 距离最近单词的集合
    '''
    # print("word", word)
    minDis = 100
    corList = []
    for key in invertedIndex:
        if string_distance(word, key) < minDis and word!=key:
            # print("key: ",key)
            minDis = string_distance(word, key)
            corList = [key]
            # print('list: ',corList)
        elif string_distance(word, key) == minDis:
            corList.append(key)
            # print('list: ',corList)
    # print('corList: ', corList)
    return corList

def mostFre(words, invertedIndex):
    '''
    从单词集合中挑选出现频率最高的单词
    :param words: 可能单词的集合
    :param invertedIndex: 倒排索引表
    '''
    print("words: ", words)
    most = len(invertedIndex[words[0]])
    word = words[0]
    for i in range(1,len(words)):
        if len(invertedIndex[words[i]]) > most:
            word = words[i]
            most = len(invertedIndex[words[i]])

    return word


def correct(str, invertedIndex):
    '''
    拼写校正
    :param str: 输入的单词
    :param invertedIndex: 倒排索引表
    :return: 将拼写错误的距离最短的频率最高的相近词返回
    '''
    return mostFre(findMin(str, invertedIndex), invertedIndex)
