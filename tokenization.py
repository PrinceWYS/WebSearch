from lib2to3.pgen2 import token
import re
from nltk.stem.porter import PorterStemmer


def queryTokenize(inputStr):
    return tokenize(inputStr, False)


def tokenize(inputStr, bracket = True):
    '''
    处理输入的字符串，将其词条化
    inputStr : 字符串
    return : 词条列表
    '''

    # TODO
    # 词条归一化 ： 关联关系法，通过wordNet实现
    # 词性归并 ： 将不同时态的词项合并为一个词项
    # 词干还原 ：将词项规约为词干


    termList = []
    for term in re.split(r'[;:!?\/\s\.]\s*',inputStr):  # 按照空格与标点进行分割
        if len(term) == 0:
            continue

        if bracket == True:
            term = term.strip('()')
        term = term.strip('<>')
        term = term.strip('[]')
        
        # 去除末尾的逗号
        term = term.rstrip(',')

        # 去除特殊字符
        term = term.strip('&')

        # 转换为小写
        term = term.lower()

        # 词干还原
        if '*' not in term:
            term = PorterStemmer().stem(term)

        termList.append(term)

    return termList