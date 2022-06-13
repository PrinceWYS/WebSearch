res1 = []   # 正向B-树搜索结果
res2 = []   # 反向B-树搜索结果

class Node(object):
    """这是一个结点类"""
    def __init__(self, n=0,isleaf = True):
        #节点关键字数量n
        self.n = n
        #关键字keys值
        self.keys = []
        # 孩子节点
        self.childs = []
        #是否是叶子节点
        self.leaf = isleaf
    @classmethod
    def allocate_node(self, key_max):
        '''
        创造结点
        :param key_max: 结点中关键词的最大数量
        :return: 结点
        '''
        node = Node()
        child_max = key_max+1
        #初始化key and child
        for i in range(key_max):
            node.keys.append(None)
        for i in range(child_max):
            node.childs.append(None)
        return node    


class BTree(object):
    """B-树类"""
    def __init__(self, t=3, root=None):
        # B数的最小度数
        self.t = t
        #节点包含的关键字的最大个数
        self.max_key = 2*self.t-1
        #节点包含的最大孩子个数
        self.max_child = self.max_key+1
        #跟节点
        self.root = root

    def btree_split_child(self, x, i):
        '''
        输入一个非满的内部节点 x 和一个使 x.child[i] 为 x 的满子节点的下标i
        把子节点分裂成两个,并调整 x
        :param x: 非满的内部结点
        :param i: 下标

        '''
        #分配一个新节点
        #z = Node()
        z = self.__new_node()
        #获取x的第i个孩子节点
        y = x.childs[i]
        #更新新生成的节点z
        z.leaf = y.leaf
        #分裂, y关键字2t-1变成t-1，z获取y中最右边的t-1个关键字
        z.n = self.t-1    
        #把y的t-1个关键字以及相应的t个孩子赋值z
        for j in range(self.t-1):
            z.keys[j] = y.keys[j+self.t]    
        if not y.leaf:
            for j in range(self.t):
                z.childs[j] = y.childs[j+self.t]

        #调整y的关键字个数
        y.n = self.t - 1
        # z插入为x的一个孩子
        for j in range(x.n+1, i, -1):
            x.childs[j] = x.childs[j-1]
        x.childs[i+1] = z
        #提升y的中间关键字到x来分割y和z
        for j in range(x.n, i-1, -1):
            x.keys[j] = x.keys[j-1]
        x.keys[i] = y.keys[self.t-1]
        #调整x的关键字个数
        x.n = x.n+1    
        
    def btree_insert_nonfull(self, x, k):
        '''
        将关键字 k 插入到节点 x 中,假定在调用过程中x是非满的
        :param x: 结点
        :param k: 关键字
        '''
        i = x.n
        #x是叶子节点，直接插入
        if x.leaf:
            while i>=1 and k<x.keys[i-1]:
                x.keys[i] = x.keys[i-1]
                i-=1
            x.keys[i] = k
            #更新节点数
            x.n+=1
        #非叶节点
        else:
            while i>=1 and k<x.keys[i-1]:
                i-=1
            i+=1
            #判断是否递归降至一个满子节点
            if x.childs[i-1].n == 2*self.t-1:
                self.btree_split_child(x,i-1)
                #确定向两个孩子中哪个下降是正确的
                if k>x.keys[i-1]:
                    i+=1
            #递归地将k插入合适的子树中    
            self.btree_insert_nonfull(x.childs[i-1],k)
    
    def __new_node(self):
        '''
        创建新的B树节点
        '''
        return Node().allocate_node(self.max_key)    

    def btree_insert(self, k):
        '''
        插入,利用btree_insert_child保证递归始终不会降至一个满节点
        :param k: 插入的关键字
        '''
        # 检查是否为空树
        if self.root is None:
            node = self.__new_node()
            self.root = node    
        r = self.root
        #根节点是满节点
        if r.n == 2*self.t - 1:
            #s = Node()
            s = self.__new_node()
            # s成为新的根节点
            self.root = s
            s.leaf = False
            s.n = 0
            s.childs[0] = r
            #分裂根节点，对根进行分裂是增加b树高度的唯一途径
            self.btree_split_child(s,0)
            self.btree_insert_nonfull(s,k)
        else:
            self.btree_insert_nonfull(r,k)

    def btree_walk(self):
        '''
        层序遍历B-树
        '''
        current = [self.root]
        while current:
            next_current = []
            output = ""
            for node in current:
                if node !=None and node.childs:
                    next_current.extend(node.childs)
                if node !=None:
                    output += '['
                    output+=' '.join(node.keys[0:node.n])
                    output+=']'
            print(output)
            print("-----")
            current = next_current

    def btree_order(self, tree):
        '''
        中序遍历B-树
        :param tree: 当前结点
        '''
        if tree is not None:
            for i in range(tree.n):
                self.btree_order(tree.childs[i])
                print(tree.keys[i],end=" ")
                self.btree_order(tree.childs[i+1])
    
    def btree_search(self,x, k):
        '''
        准确查找
        :param x: 当前结点
        :param k: 查找的值
        :return: 查找结果
        '''
        i = 0
        while i<=x.n and k > x.keys[i]:
            i+=1
        # 检查是否已经找到关键字
        if i < x.n and k == x.keys[i]:
            return (x,i)
        #没找到，若是叶子节点，则查找不成功
        elif x.leaf:
            return None
        #非叶子节点，继续递归查找孩子节点
        else:
            return self.btree_search(x.childs[i],k)
    
    def search_pre(self, x, str):
        '''
        搜做正序B-树
        :param x: 当前结点
        :param str: 搜索的目标
        '''
        global res1
        i = 0
        if x==None:
            return
        while i <x.n and x.keys[i]!=None and str > x.keys[i]:
            i += 1
        if i<x.n:
            if x.keys[i].startswith(str):
                res1.append(x.keys[i])
            while i<=x.n:
                self.search_pre(x.childs[i], str)
                i += 1
                if i<x.n and x.keys[i].startswith(str):
                    res1.append(x.keys[i])
        else:
            while i<=x.n:
                self.search_pre(x.childs[i], str)
                i += 1

    def search_pro(self, x, str):
        '''
        :param x: 当前结点
        :param str: 搜索目标
        '''
        global res2
        i = 0
        if x==None:
            return
        while i <x.n and x.keys[i]!=None and str > x.keys[i]:
            i += 1
        if i<x.n:
            if x.keys[i].startswith(str):
                res2.append(x.keys[i][::-1])
            while i<=x.n:
                self.search_pro(x.childs[i], str)
                i += 1
                if i<x.n and x.keys[i].startswith(str):
                    res2.append(x.keys[i][::-1])
        else:
            while i<=x.n:
                self.search_pro(x.childs[i], str)
                i += 1

tree1 = BTree() # 正序B-树
tree2 = BTree() # 逆序B-树

def buildTree(invertedIndex):
    '''
    建立B-树
    :param invertedIndex: 倒排索引表
    '''
    global tree1
    global tree2
    # invertedIndex.invert()
    for key in invertedIndex:
        tree1.btree_insert(key)
        tree2.btree_insert(key[::-1])
