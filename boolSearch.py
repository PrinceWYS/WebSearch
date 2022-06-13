import stack
import invertedIndex
import globbing
import correct
import indexCompression
import re
import phraseQuery
import synonymExpansion
import tokenization

def isPhrase(word, invertedIndex, posIndex):
    '''
    根据是单词或短语返回列表
    :param word: 输入的单词或短语
    :param invertedIndex: 索引表
    :return: 对应的索引表
    '''
    # print("word", word, ' ', len(word))
    # 短语 进行同义词扩展
    if len(word) > 1:

        return phraseQuery.phraseQuery(word, posIndex)
    elif len(word) == 1:
        # print(word[0])
        l = word[0]
        # 如果含有通配符, 加上通配查询的词汇索引
        if '*' in l:
            return globbing.Glob(l,invertedIndex)
        # 如果查询不存在, 检查拼写错误
        elif len(invertedIndex[l]) == 0:
            print('您所搜寻的', l, '无结果')
            print('正在进行拼写校正...')
            may = correct.correct(l, invertedIndex)
            print('您是否搜寻的是: ',may)
            return indexCompression.restoreDocId(may, invertedIndex)
        # 否则加上该词汇同义词扩展的索引
        else:
            return indexCompression.restoreDocId(l, invertedIndex)
            # print("bug, ",synonymExpansion.synonymPhraseQuery(word, invertedIndex))
            # return synonymExpansion.synonymPhraseQuery(word, invertedIndex)

def invertList(list, invertedIndex, posIndex):
    '''
    将词汇列表转换成索引列表
    :param list: 词汇列表
    :param invertedIndex: 倒排索引表
    :return: 返回索引列表
    '''
    resList = []
    temp = []
    for l in list:
        # 如果是逻辑运算符或者括号, 保留
        if l=='and' or l=='not' or l=='or' or l=='(' or l==')':
            if len(temp) >=1:
                # print(temp)
                resList.append(isPhrase(temp, invertedIndex, posIndex))
            resList.append(l)
            temp = []
        else:
            temp.append(l)
    if len(temp) >= 1:
        resList.append(isPhrase(temp, invertedIndex, posIndex))
    # print(resList)
    return resList

def pior(a, b):
    '''
    判断两个运算符的优先级
    :param a: 第一个运算符
    :param b: 第二个运算符
    :return: 前者优先级高返回false, 否则返回true
    '''
    if b=='(':
        return False
    if a=='NOT':
        if b=='AND' or b=='OR':
            return False
        else:
            return True
    if a=='AND':
        if b=='OR':
            return False
        else:
            return True
    return True

def cal(list):
    '''
    对输入的布尔中缀表达式进行计算
    :param list: 表达式的列表形式
    :return: 计算结果
    '''
    num = stack.Stack() # 数字栈 存储词汇索引
    sym = stack.Stack() # 符号栈 存储逻辑运算符和括号
    for l in list:
        if l == '(' :   # 左括号
            sym.push(l)
        elif l == ')' : # 右括号
            while sym.peek() != '(':
                num.push(sym.peek())
                sym.pop()
            sym.pop()
        elif l!='and' and l!='or' and l!='not' : # 普通字符
            num.push(l)
        else:   # 布尔运算符
            if sym.is_empty()==True:
                sym.push(l)
            else:
                if pior(l, sym.peek())==False:
                    sym.push(l)
                else:
                    while sym.is_empty()==False and pior(l, sym.peek())==True :
                        num.push(sym.peek())
                        sym.pop()
                    sym.push(l)
    while sym.is_empty()==False:
        num.push(sym.peek())
        sym.pop()
    
    # 将数字栈逆转方便求结果
    num.reverse()

    res = stack.Stack()
    while num.is_empty()==False:
        # 取出栈顶的两个元素做 AND 或者 OR 操作
        if num.peek()=='and' or num.peek()=='or':
            a = res.peek()
            res.pop()
            b = res.peek()
            res.pop()
            if num.peek()=='and':
                res.push(doAnd(a,b))
            else:
                res.push(doOr(a, b))
        # 取出栈顶的一个元素做 NOT 操作
        elif num.peek()=='not':
            a = res.peek()
            res.pop()
            res.push(doNot(a))
        # 将数字栈的元素压入结果栈
        else:
            res.push(num.peek())
        num.pop()

    return res.peek()

def doAnd(a, b):
    '''
    对两个索引求交集
    :param a: 第一个索引
    :param b: 第二个索引
    :return: 二者交集
    '''
    andList = []
    for aList in a:
        if aList in b:
            andList.append(aList)
    return andList

def doOr(a, b):
    '''
    对两个索引求并集
    :param: 第一个索引
    :param: 第二个索引
    :return: 二者并集
    '''
    orList = []
    for aList in a:
        orList.append(aList)
    for bList in b:
        if bList in orList:
            continue
        else:
            orList.append(bList)
    # 对结果进行排序
    orList = sorted(orList)
    return orList

def doNot(a):
    '''
    对索引求补集
    :param: 目标索引
    :return: 索引补集
    '''
    notList = []
    # print(len(invertedIndex.fileList))
    for aList in invertedIndex.fileList:
        if aList in a:
            continue
        else:
            notList.append(aList)
    return notList

def Bool(str, invertedIndex, posIndex):
    '''
    对传入字符串进行布尔查询(含通配和拼写校正)
    :param str: 输入查询项目
    :param invertedIndex: 倒排索引表
    :return: 查询结果
    '''
    list = tokenization.queryTokenize(str)# 将输入以空格分割
    # print(list)
    inList = invertList(list, invertedIndex, posIndex) # 将词汇列表转为索引列表
    res = cal(inList)   # 对索引列表进行逻辑运算
    res = sorted(res)   # 对结果进行排序
    # print("res: ", len(res))
    # print(res)
    return res