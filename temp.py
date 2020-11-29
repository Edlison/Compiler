# @Author  : Edlison
# @Date    : 11/29/20 23:58

import sys
import operator
import copy

#终结符
terSymbol = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
             '+','-','*','/','(',')','^','#']
#非终结符
non_ter = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

firstVT = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
lastVT = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

#求firstVT集
def first(gra_line):
    #开头的非终结符，所以求的是x的firstVT
    x = gra_line[0]
    ind = non_ter.index(x)
    indexSET = []
    # 找到所有产生式右部的第一个字符，下标值返回列表indexSET
    i = 0
    while i < len(gra_line):
        if gra_line[i] == '>' or gra_line[i] == '|':
            indexSET.append(i + 1)
        i += 1
    #判断符合P->a...或P->Qa...，以及P->Q...那个情况，注意gra_line[i]是当前遍历的字符
    for i in indexSET:
        if gra_line[i] in terSymbol and gra_line[i] not in firstVT[ind]:
            firstVT[ind].append(gra_line[i])
        elif gra_line[i] in non_ter:
            for f in firstVT[non_ter.index(gra_line[i])]:
                if f not in firstVT[ind]:
                    firstVT[ind].append(f)
            if gra_line[i + 1] in terSymbol and gra_line[i + 1] not in firstVT[ind]:
                firstVT[ind].append(gra_line[i + 1])
    return firstVT


#求lastVT集
def last(gra_line):
    # 开头的非终结符，所以求的是x的lastVT
    x = gra_line[0]
    ind = non_ter.index(x)
    indexSET = []
    # 找到所有产生式右部的最后一个字符，下标值返回列表indexSET
    i = 0
    while i < len(gra_line):
        if gra_line[i] == '|' or gra_line[i] == '\n':
            indexSET.append(i - 1)
        i += 1
    # 判断符合P->...a或P->...aQ，以及P->...Q那个情况，注意gra_line[i]是当前遍历的字符
    for i in indexSET:
        if gra_line[i] in terSymbol and gra_line[i] not in lastVT[ind]:
            lastVT[ind].append(gra_line[i])
        elif gra_line[i] in non_ter:
            for f in lastVT[non_ter.index(gra_line[i])]:
                if f not in lastVT[ind]:
                    lastVT[ind].append(f)
            if gra_line[i - 1] in terSymbol and gra_line[i - 1] not in lastVT[ind]:
                lastVT[ind].append(gra_line[i - 1])
    return lastVT


#求每一个产生式的右部单独的产生式
def prostr(grammer):
    pro_str = []
    for gra_line in grammer:
        #先看每一行有几个产生式，把每一个产生式的开始索引加入pro_index
        pro_index = []
        i = 0
        while i < len(gra_line):
            if gra_line[i] == '>' or gra_line[i] == '|':
                pro_index.append(i + 1)
            i += 1
        for p in pro_index:
            str = ''
            for s in gra_line[p:]:
                if s == '|' or s == '\n':
                    break
                else:
                    str = str + s
            pro_str.append(str)
    return pro_str


#构造优先关系表
def table(grammer, num):
    #表头
    n = len(num) + 1
    #创建一个n行n列的空表
    gra = [[' ' for col in range(n)] for row in range(n)]
    #填充表头
    i = 1
    for c in num:
        gra[0][i] = c
        i += 1
    j = 1
    for r in num:
        gra[j][0] = r
        j += 1
    #填充表体
    pro_str = prostr(grammer)
    for str in pro_str:
        if str == '@':
            continue
        else:
            j = -1
            for i in str[:-1]:
                #i是当前元素，j是当前索引
                j += 1
                if i in terSymbol and str[j + 1] in terSymbol:
                    r = num.index(i) + 1
                    c = num.index(str[j + 1]) + 1
                    if gra[r][c] == '·>' or gra[r][c] == '<·':
                        print("该文法不是算符优先文法，请检查输入")
                        return False
                    else:
                        gra[r][c] = '=·'
                if j < (len(str) - 2) and i in terSymbol and str[j + 2] in terSymbol and str[j + 1] in non_ter:
                    r = num.index(i) + 1
                    c = num.index(str[j + 2]) + 1
                    if gra[r][c] == '·>' or gra[r][c] == '<·':
                        print("该文法不是算符优先文法，请检查输入")
                        return False
                    else:
                        gra[r][c] = '=·'
                if i in terSymbol and str[j + 1] in non_ter:
                    for a in firstVT[non_ter.index(str[j + 1])]:
                        r = num.index(i) + 1
                        c = num.index(a) + 1
                        if gra[r][c] == '·>' or gra[r][c] == '=·':
                            print("该文法不是算符优先文法，请检查输入")
                            return False
                        else:
                            gra[r][c] = '<·'
                if i in non_ter and str[j + 1] in terSymbol:
                    for a in lastVT[non_ter.index(i)]:
                        r = num.index(a) + 1
                        c = num.index(str[j + 1]) + 1
                        if gra[r][c] == '=·' or gra[r][c] == '<·':
                            print("该文法不是算符优先文法，请检查输入")
                            return False
                        else:
                            gra[r][c] = '·>'
    #添加#的行和列元素
    for a in firstVT[non_ter.index(grammer[0][0])]:
        r = num.index('#') + 1
        c = num.index(a) + 1
        gra[r][c] = '<·'
    for a in lastVT[non_ter.index(grammer[0][0])]:
        r = num.index(a) + 1
        c = num.index('#') + 1
        gra[r][c] = '·>'
    r = num.index('#') + 1
    c = num.index('#') + 1
    gra[r][c] = '=·'
    return gra


#归约函数
def reduce(str):
    #str是传进来的最左素短语
    p_s = prostr(grammer)
    for s in p_s:
        if len(s) != len(str):
            continue
        else:
            j = 0
            for i in s:
                #如果是最后一个字符相比较了
                if j + 1 == len(str):
                    if i in terSymbol and str[j] in terSymbol and i == str[j]:
                        return True
                    elif i in non_ter and str[j] in non_ter:
                        return True
                else:
                    if i in terSymbol and str[j] in terSymbol and i == str[j]:
                        j += 1
                    elif i in non_ter and str[j] in non_ter:
                        j += 1
                    else:
                        break
    return False


#总控程序
def master(ana_str, num):
    stack = ['#']
    ana_str += '#'
    print("当前栈中元素为：")
    print(stack)
    print("当前字符串为：")
    print(ana_str)
    while stack != ['#','N','#']:
        if ana_str == '#':
            stack.append('#')
            print("移进#")
            print()
            print("当前栈中元素为：")
            print(stack)
            continue
        #字符串第一个字符是非终结符，则加入栈
        if ana_str[0] in non_ter:
            stack.append(ana_str[0])
            print("移进" + ana_str[0])
            print()
            print("当前栈中元素为：")
            print(stack)
            ana_str = ana_str[1:]
            print("当前字符串为：")
            print(ana_str)
        #j是stack中最上面终结符的下标
        if stack[-1] in terSymbol:
            j = len(stack) - 1
        else:
            j = len(stack) - 2
        #stack[j]是栈最上面的终结符,a是当前输入串的第一个字符（终结符
        a = ana_str[0]
        if stack[j] not in num or a not in num:
            print("ERROR")
            return False
        else:
            #栈顶终结符优先级低于等于字符串第一个终结符
            if gra[num.index(stack[j]) + 1][num.index(a) + 1] == '<·' or gra[num.index(stack[j]) + 1][num.index(a) + 1] == '=·':
                stack.append(a)
                print("移进" + a)
                print()
                print("当前栈中元素为：")
                print(stack)
                ana_str = ana_str[1:]
                print("当前字符串为：")
                print(ana_str)
                if ana_str[0] in non_ter:
                    stack.append(ana_str[0])
                    print("移进" + ana_str[0])
                    print()
                    print("当前栈中元素为：")
                    print(stack)
                    ana_str = ana_str[1:]
                    print("当前字符串为：")
                    print(ana_str)
                j += 1
                if stack[j] in non_ter:
                    j += 1
                a = ana_str[0]
            if stack[j] not in num or a not in num:
                print("ERROR")
                return False
            else:
                #如果栈顶终结符优先级高于字符串第一个终结符
                while gra[num.index(stack[j]) + 1][num.index(a) + 1] == '·>':
                    #寻找最左素短语
                    str = ''
                    if ana_str[0] in non_ter:
                        str += ana_str[0]
                        ana_str = ana_str[1:]
                    #如果栈顶是非终结符
                    if stack[-1] in non_ter:
                        str += stack[-1]
                    while j >= 1:
                        #j是往下遍历的指针,b是减小之前的
                        #b记录当前栈顶非终结符，并将b加入最左素短语
                        b = stack[j]
                        str += b
                        #如果当前终结符的下一个是终结符，指向下一个，否则指向下下一个
                        if stack[j - 1] in terSymbol:
                            j -= 1
                        else:
                            str += stack[j - 1]
                            j -= 2
                        #如果下一个终结符优先级小于当前终结符
                        if gra[num.index(stack[j]) + 1][num.index(b) + 1] == '<·':
                            break
                    str = str[::-1]
                    #归约,str是最左素短语
                    if reduce(str) == True:
                        print("将" + str + "归约为N")
                        print()
                        del stack[len(stack) - len(str):]
                        stack.append('N')    #反正模糊归约，这个非终结符随便写个就行了8
                        print("当前栈中元素为：")
                        print(stack)
                        print("当前字符串为：")
                        print(ana_str)
                    else:
                        print("归约失败")
                        break
                if gra[num.index(stack[j]) + 1][num.index(a) + 1] != '·>'\
                    and gra[num.index(stack[j]) + 1][num.index(a) + 1] != '=·'\
                    and gra[num.index(stack[j]) + 1][num.index(a) + 1] != '<·':
                    print("ERROR")
                    return False
                #j已经指向栈顶第一个终结符
    return True


#比较两个嵌套列表是否相等
def cmp(SET1, SET2):
    i = 0
    while i < 26:
        if (operator.eq(SET1[i], SET2[i])) == False:
            return False
        else:
            i += 1
    return True


if __name__ == '__main__':
    ana_str = input("请输入一个待分析的串：")
    print("请输入一个文法：")
    grammer = sys.stdin.readlines()

    #循环求最终firstVT集
    first1 = copy.deepcopy(firstVT)
    for gr in grammer:
        first(gr)
    first2 = copy.deepcopy(firstVT)

    while not cmp(first1, first2):
        first1 = copy.deepcopy(firstVT)
        for gr in grammer:
            first(gr)
        first2 = copy.deepcopy(firstVT)

    print("该文法的非终结符的firstVT集为：")
    i = 0
    for f in firstVT:
        if len(f) != 0:
            print('firstVT(' + non_ter[i] + '):', f)
        i += 1
    print()

    # 循环求最终lastVT集
    last1 = copy.deepcopy(lastVT)
    for gr in grammer:
        last(gr)
    last2 = copy.deepcopy(lastVT)

    while not cmp(last1, last2):
        last1 = copy.deepcopy(lastVT)
        for gr in grammer:
            last(gr)
        last2 = copy.deepcopy(lastVT)

    print("该文法的非终结符的lastVT集为：")
    j = 0
    for f in lastVT:
        if len(f) != 0:
            print('lastVT(' + non_ter[j] + '):', f)
        j += 1
    print()

    num = []
    for gra_line in grammer:
        for gr in gra_line:
            if gr == '-' and gra_line.index(gr) == 1:
                continue
            elif gr in terSymbol and gr not in num:
                num.append(gr)
    num.append('#')

    if table(grammer,num) != False:
        print("该文法的优先关系表为：")
        gra = table(grammer, num)
        for i in range(len(gra)):  # 控制行
            for j in range(len(gra[i])):  # 控制列
                print(gra[i][j], end='\t')
            print()
        print()

        print("分析过程如下：")
        print()
        if master(ana_str, num) == True:
            print("接受")