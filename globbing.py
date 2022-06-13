import BTree
import boolSearch
import indexCompression

def splitToPart(str):
    '''
    将字符串按照 * 分割
    :param str: 传入的字符串
    :return: 分割后词项集合 
    '''
    word = []
    a = ''
    # print(str)
    for i in range(len(str)):
        if str[i]=='*':
            a = a + str[i]
            if i!=0:
                # print(a)
                word.append(a)
                a = '*'
        else:
            a = a + str[i]
    if a!='*':
        word.append(a)
    return word

def index(word, invertedIndex):
    '''
    将分割后的每个词求可能的词项集合
    :param word: 需要求的词项
    :param invertedIndex: 索引表
    :return: 词项集合
    '''
    words = []
    # *a 形式, 以 a 结尾
    if word.startswith('*') and not word.endswith('*'):
        # print(word[1:])
        BTree.res2 = []
        BTree.tree2.search_pro(BTree.tree2.root,(word[1: ])[::-1])
        words = BTree.res2
        return words
    # a* 形式, 以 a 开头
    elif not word.startswith('*') and word.endswith('*'):
        # print(word[:len(word)-1])
        BTree.res1 = []
        BTree.tree1.search_pre(BTree.tree1.root,word[:len(word)-1])
        words = BTree.res1
        return words 
    # *a* 形式, 含有 a
    elif word.startswith('*') and word.endswith('*'):
        temp = word[1:len(word)-1]
        for key in invertedIndex:
            if temp in key:
                words.append(key)
        return words
    # 准确查询
    else:
        return [word]

def findIndex(list, invertedIndex):
    '''
    对于一个通配分词求索引集合
    :param list: 一个通配词的可能集合
    :param invertedIndex: 倒排索引表
    :return: 该通配分词的索引集合
    '''
    indexList = []
    for key in list:
        indexList.append(indexCompression.restoreDocId(key, invertedIndex))
    return indexList

def merge(list):
    '''
    合并可能词
    :param list: 各部分可能词列表
    :return: 通配查询的可能词
    '''
    result = list[0]
    for i in range(1, len(list)):
        result = boolSearch.doAnd(result, list[i])
    return result

def mergeIndex(list):
    '''
    将所有可能词的索引表合并
    :param list: 各个可能词索引
    :return: 通配查询结果健康
    '''
    if len(list)==0:
        return []
    result = list[0]
    for i in range(1, len(list)):
        result = boolSearch.doOr(result, list[i])
    return result 


def Glob(str, invertedIndex):
    wordList = splitToPart(str)
    # print(wordList)
    indexList = []
    for word in wordList:
        indexList.append(index(word, invertedIndex))
    res = merge(indexList)
    resIndex = mergeIndex(findIndex(res, invertedIndex))
    print("符合条件的词项有: ", res)
    # print("glob:", resIndex)

    return resIndex

# Glob()
