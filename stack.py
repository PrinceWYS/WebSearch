class Stack:
    # initial blank stack
    def __init__(self, size=100):
        self.stack = []
        self.size = size
        self.top = -1
    
    # 判断堆栈是否为空
    def is_empty(self):
        return self.top == -1
    
    # 判断栈是否已满
    def is_full(self):
        return self.top + 1 == self.size
    
    # 入栈操作
    def push(self,val):
        if self.is_full():
            raise Exception("Stack is full")
        else:
            self.top += 1
            self.stack.append(val)
    
    # 出栈操作
    def pop(self):
        if self.is_empty():
            raise Exception("Stack is empty")
        else:
            self.top -= 1
            self.stack.pop()
    
    # 获取栈顶元素
    def peek(self):
        if self.is_empty():
            raise Exception("Stack is empty")
        else:
            return self.stack[self.top]
    
    # 逆转栈
    def reverse(self):
        temp = []
        while self.is_empty()==False:
            # print(self.peek())
            temp.append(self.peek())
            self.pop()
        # print("temp",temp)
        for ele in temp:
            # print(ele)
            self.push(ele)
