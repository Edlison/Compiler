# @Author  : Edlison
# @Date    : 11/17/20 00:11
import os
from compiler_exception import GrammarAnalyseException


class AnalyseStack:
    def __init__(self):
        self.top = 0
        self.s = ''


class GrammarAnalyzer:
    def __init__(self, table_path, text_path):
        self.text = ''
        self.table = []
        self.analyse_stack = []

        self._load_text(text_path)
        self._load_table(table_path)

    def _load_text(self, path):
        if not os.path.exists(path):
            raise GrammarAnalyseException('文件不存在')
        with open(path) as f:
            text = f.read()
        self.text = text

    def _load_table(self, path):
        if not os.path.exists(path):
            raise GrammarAnalyseException('文件不存在')
        with open(path) as f:
            table = f.read()
        self.table = eval(table)

    def isVT(self, c):
        flag = False
        for i in range(len(self.table[0])):
            if c == self.table[0][i]:
                flag = True
        return flag

    def _query_table(self, ch1, ch2):
        i, j = 0, 0

        if ch1 == '+':
            i = 1
        elif ch1 == '*':
            i = 2
        elif ch1 == '-':
            i = 3
        elif ch1 == 'i':
            i = 4
        elif ch1 == '(':
            i = 5
        elif ch1 == ')':
            i = 6
        elif ch1 == '#':
            i = 7
        else:
            raise GrammarAnalyseException('查询优先表失败')

        if ch2 == '+':
            j = 1
        elif ch2 == '*':
            j = 2
        elif ch2 == '-':
            j = 3
        elif ch2 == 'i':
            j = 4
        elif ch2 == '(':
            j = 5
        elif ch2 == ')':
            j = 6
        elif ch2 == '#':
            j = 7
        else:
            raise GrammarAnalyseException('查询优先表失败')

        if self.table[i][j] == '>':
            return 1
        elif self.table[i][j] == '<':
            return -1
        elif self.table[i][j] == '=':
            return 0
        else:
            return 2

    def analyse(self):
        # 初始化
        self.analyse_stack.append('#')
        top = len(self.analyse_stack) - 1
        top_vt = top
        cur = 0
        input_len = 0
        ch = ''
        text = self.text

        while True:
            ch = text[cur]
            # 特殊情况判断
            if ch == '*' and text[cur + 1] == '*':
                ch = '-'
                cur += 1
            # 分析栈顶的终结符
            if self.isVT(self.analyse_stack[top]):
                top_vt = top
            else:
                top_vt = top - 1

            # TODO 优先级大的规约
            while self.isVT(ch) and self._query_table(self.analyse_stack[top_vt], ch) == 1:
                pass

            # TODO 优先级小于等于移进
            if self._query_table(self.analyse_stack[top_vt], ch) == 2:
                pass
            else:
                pass




if __name__ == '__main__':
    ga = GrammarAnalyzer('','')
    ga._load_table('./priority_table.txt')
    print(ga.table)