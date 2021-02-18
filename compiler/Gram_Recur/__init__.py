
class Gram_R():
    def __init__(self,url):
        self.token = '' #将要识别的字符存放到token
        self.get_exper(url)
        self.current = ''
        self.current = self.token[0]

    def E(self):
        if self.current == '(' or self.current == 'i':
            if self.T():
                if self.E_1():
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def E_1(self):
        if self.current == '+' or self.current == '-':
            if self.A():
                if self.T():
                    if self.E_1():
                        return  True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            if self.current == ')' or self.current == '#':
                return True
            else:
                return False

    def T(self):
        if self.current == 'i' or self.current == '(':
            if self.F():
                if self.T_1():
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def T_1(self):
        if self.current == '*' or self.current == '/' :
            if self.M():
                if self.F():
                    if self.T_1():
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        elif self.current == ')' or self.current == '#' or self.current == '+' or self.current == '-':
            return True
        else:
            return False

    def M(self):
        if self.current == '*' or self.current == '/':
            self.advance()
            return True
        else:
            return False

    def A(self):
        if self.current == '+' or self.current == '-':
            self.advance()
            return True
        else:
            return False

    def F(self):
        if self.current == '(':
            self.advance()
            if self.E():
                if self.current == ')':
                    self.advance()
                    return True
                else:
                    return False
            else:
                return False
        elif self.current == 'i':
            self.advance()
            return  True
        else:
            return False

    def advance(self):
        self.token = self.token[1:]
        self.current = self.token[0]

    def get_exper(self,url):
        with open(url,'r') as f:
            tokens = f.readline()
            f.close()

        l = list(tokens) #将字符串转换成列表
        for i in range(len(tokens)): #可以识别任意名字的标识符
            if i%5 == 1:
                if tokens[i] == '1':
                    l[i+2] = 'i'
        print(l)

        NewTokens = ''.join(l)
        for i in range(len(NewTokens)):
            if i%5 == 3:
                self.token += NewTokens[i]



if __name__ == '__main__':
    url = ''

    while(True):
        i = input('1 output.txt\n2 error1.txt\n3 error2.txt\n4 error3.txt\n5 退出\n输入要识别的表达式：')
        i = int(i)
        if i == 1:
            url = 'output.txt'
        elif i == 2:
            url = 'error1.txt'
        elif i == 3:
            url = 'error2.txt'
        elif i == 4:
            url = 'error3.txt'
        elif i == 5:
            print('退出！\n')
            break

        gram = Gram_R(url)
        # gram.get_exper(url)
        print(gram.token)
        if gram.E():
            print('SuccessFul!\n')
        else:
            print("Error!\n")