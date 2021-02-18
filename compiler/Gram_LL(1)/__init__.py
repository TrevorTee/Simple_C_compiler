
class Gram_L():

    def __init__(self, url):
        self.url = url #file name
        self.token = ''
        self.get_exper(self.url)#得到表达式
        #self.token = '++1#'
        self.Lan = {} #生成文法
        self.get_Lan()

        self.First = {}
        self.get_First()
        self.Follow = {}
        self.get_Follow()
        print(self.First)
        print(self.Follow)

        self.VT = [] #终结符号集
        self.AnalyTab = {}#分析表
        self.get_AnalyseTab()

        self.analyse()


    def get_Lan(self):
        self.Lan = {
            'E':['TG'],
            'G':['ATG','e'],
            'T':['FH'],
            'H':['MFH','e'],
            'F':['(E)','i'],
            'A':['+','-'],
            'M':['*','/']
        }

    def get_First(self):

        for lan in self.Lan:
            ls = self.Lan[lan]
            self.First[lan] = []
            for s in ls:
                if not (s[0].isupper()):
                    self.First[lan].append(s[0])
        #两遍求first集，第一遍时产生式右边首字符为终结符号
        for t in range(2):
            for lan in self.Lan:
                ls = self.Lan[lan]
                for s in ls:
                    if s[0].isupper():
                        self.First[lan].extend(self.First[s[0]])
                        self.First[lan] = list(set(self.First[lan]))

    def get_Follow(self):
        condition = lambda t: t != 'e' #除去空

        for lan in self.Lan:
            self.Follow[lan] = []
            if lan == 'E':
                self.Follow[lan].append('#')

        for i in range(2):
            for lan in self.Lan:
                lf  = self.Lan[lan]
                for s in lf:
                    inde  = len(s)
                    if s[inde - 1].isupper():
                        self.Follow[s[inde - 1]].extend(self.Follow[lan]) # 若A→αB是一个产生式，则把FOLLOW(A)加至FOLLOW(B)中
                        self.Follow[s[inde - 1]] = list(filter(condition, self.Follow[s[inde - 1]]))  # 除去空

                    for index in range(len(s) - 1):
                        if s[index].isupper():
                            if s[index + 1].isupper():# 若A→αBβ是一个产生式，则把FIRST(β)\{ε}加至FOLLOW(B)中；
                                self.Follow[s[index]].extend(self.First[s[index + 1]])
                                self.Follow[s[index]] = list(filter(condition, self.Follow[s[index]]))

                                if 'e' in self.Lan[s[index + 1]]:# A→αBβ是一个产生式而(即ε属于FIRST(β))，则把FOLLOW(A)加至FOLLOW(B)中
                                    self.Follow[s[index]].extend(self.Follow[lan])

                            if not s[index + 1].isupper():#终结符号加入到follow集
                                self.Follow[s[index]].extend(s[index + 1])

        for k in self.Follow:#去重
            self.Follow[k] = list(set(self.Follow[k]))

    def get_VT(self):
        self.VT.append('#')
        for val in self.Lan.values():
            for str in val:
                for s in str:
                    if (not s.isupper()) and s != 'e':
                        self.VT.append(s)

        self.VT = list(set(self.VT))

    def write_table(self):#生成分析表文件
        with open('table.txt','w') as f:
            for lan in self.Lan:
                f.write(lan+str(self.AnalyTab[lan]))
                f.write('\n')

    def get_AnalyseTab(self):
        self.get_VT()

        for k in self.Lan:#初始化分析表
            self.AnalyTab[k] = {}
            for vt in self.VT:
                self.AnalyTab[k][vt] = None

        for lan in self.Lan:
            ls = self.Lan[lan]
            for exp in ls:
                if exp[0].isupper():
                    for vt in self.VT:
                        if vt in self.First[exp[0]]:
                            self.AnalyTab[lan][vt] = exp
                elif exp == 'e':
                    for vt in self.VT:
                        if vt in self.Follow[lan]:
                            self.AnalyTab[lan][vt] = exp
                elif not exp[0].isupper():
                    self.AnalyTab[lan][exp[0]] = exp

    def get_exper(self, url):
        with open(url, 'r') as f:
            tokens = f.readline()
            f.close()

        l = list(tokens)  # 将字符串转换成列表
        for i in range(len(tokens)):  # 可以识别任意名字的标识符
            if i % 5 == 1:
                if tokens[i] == '1':
                    l[i + 2] = 'i'

        NewTokens = ''.join(l)
        for i in range(len(NewTokens)):
            if i % 5 == 3:
                self.token += NewTokens[i]

    def analyse(self):
        token = self.token
        process = []
        process.append('#')
        process.append('E') #开始符号进栈

        errorflag = False#设立出错标志

        while(process[-1] != '#'):

            current = token[0]
            if(process[-1].isupper()):
                new = self.AnalyTab[process[-1]][current]
                if new == None:
                    errorflag = True
                    break

                elif len(new)>1:
                    s = len(new)-1
                    process.pop()#出栈
                    for i in range(len(new)):
                        process.append(new[s])
                        s -= 1


                elif  (not new.isupper()) and new != 'e':
                    process.pop()
                    process.append(new[0])
                    #print(process)
                    if process[-1] == current:
                        process.pop()
                        token = token[1:] #余留字符串减一
                    else:
                        errorflag = True
                        break

                elif new == 'e':
                    process.pop()
            elif process[-1]!= '#':
                if process[-1] == current:
                    process.pop()
                    token = token[1:]
                else:
                    errorflag = True
                    break



        if errorflag == False and process[-1] == token[0]=='#':
            print("Successful!")
        else:
            print('Error exp!')
            print(self.token)



        return




if __name__ == '__main__':
    url = ''

    while (True):
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

        gram_L = Gram_L(url)