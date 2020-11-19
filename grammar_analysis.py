# @Author  : Edlison
# @Date    : 11/17/20 00:11
import os

from typing import List

from compiler_exception import GrammarAnalyseException
# TODO 1.lastvt,firstvt 2.priority 3.analyse stack 生成产生式
# TODO 1.通过产生式 生成树 2.通过树进行语义分析


class AnalyseStack:
    def __init__(self):
        self.top = 0
        self.s = ''


class Grammar:
    def __init__(self, id: int, left: str, right: str):
        self.id = id  # 文法序号
        self.left = left  # 文法左半部分
        self.right = right  # 文法右半部分

        self.terminal = []
        self.non_terminal = []

        self.firstvt = []
        self.lastvt = []

        for each in right.split(' '):
            if each.isupper():
                self.non_terminal.append(each)
            else:
                self.terminal.append(each)

    def is_in_firstvt(self, s):
        for each in self.firstvt:
            if s == each:
                return True
        return False

    def is_in_lastvt(self, s):
        for each in self.lastvt:
            if s == each:
                return True
        return False

    def __str__(self):
        return 'ID: {} \t Left: {} \t Right: {} \n end: {} \n not_end: {} \n FirstVT: {} \n LastVT: {}'.format(
            self.id, self.left, self.right, self.terminal, self.non_terminal, self.firstvt, self.lastvt)


class PriorityTable:
    def __init__(self):
        self.terminal = []
        self.relation = [0, 1, 2, 3]

    def is_in_terminal(self, s):

        pass

    def terminal_index(self, s):
        pass


class GrammarAnalyzer:
    def __init__(self, grammar_table_path):
        self.text = ''
        self.grammar_table: List[Grammar] = []
        self.priority_table = PriorityTable()


        self._load_grammar_table(grammar_table_path)

    def _load_grammar_table(self, path):
        if not os.path.exists(path):
            raise GrammarAnalyseException('文法表不存在')
        with open(path) as f:
            grammar_list = f.read()
        grammar_list = eval(grammar_list)

        for each in grammar_list:
            self.grammar_table.append(Grammar(each[0], each[1], each[2]))

    def is_not_end(self, end, s):  # 判断是否是非终结符
        pass

    def find_grammar(self, t):  # 根据非终结符找文法
        pass

    def gen_firstvt_lastvt(self):
        epoch = self.grammar_table[len(self.grammar_table) - 1].id  # 拿到文法的个数
        for i in range(epoch):  # 每个文法都比对一遍
            for each in self.grammar_table:
                if i == each.id:
                    right = each.right.split(' ')
                    # firstvt
                    if right[0].islower() and right[0] is not '?':  # TODO islower还需要判断?吗
                        if not each.is_in_firstvt(right[0]):
                            each.firstvt.append(right[0])
                    else:
                        if len(right) > 1:
                            if right[1].islower():
                                if not each.is_in_firstvt(right[1]):
                                    each.firstvt.append(right[1])
                    # lastvt
                    last = len(right) - 1
                    if right[last].islower() and right[last] is not '?':
                        if not each.is_in_lastvt(right[last]):
                            each.lastvt.append((right[last]))
                    else:
                        if len(right) > 1:
                            if right[last - 1].islower():
                                if not each.is_in_lastvt(right[last - 1]):
                                    each.lastvt.append(right[last - 1])

    def gen_priority_table(self):
        # Table拿到所有终结符
        for each_grammar in self.grammar_table:
            terminal = each_grammar.terminal
            for each_terminal in terminal:
                if not self.priority_table.is_in_terminal(each_terminal) and each_terminal is not '?':
                    self.priority_table.terminal.append(each_terminal)

        row_col = len(self.priority_table.terminal)
        table = [[0 for row in range(row_col)] for col in range(row_col)]
        for each_grammar in self.grammar_table:
            right = each_grammar.right.split(' ')
            for index, each_ch in enumerate(right[:-2]):  # 只到倒数第二个
                if each_ch.isupper():  # 是非终结符 >
                    lastvt = []
                    for each_grammar_ in self.grammar_table:
                        if each_grammar_.non_terminal == each_ch:  # TODO 文法的nonterminal有多个 == each_ch??
                            lastvt.append(each_grammar_.lastvt)
                            break
                    for i in lastvt:
                        row = self.priority_table.terminal.index(i)
                        col = self.priority_table.terminal.index(right[index + 1])
                        table[row][col] = 3
                else:  # 是终结符
                    if right[index + 1].isupper():  # 第二个是非终结符 <
                        pass
                        if (index + 2) < len(right) and right[index + 2].islower():  # 看第三个如果是终结符 =
                            pass
                    else:  # 第二个是终结符 =
                        pass
            for index, each_ch in enumerate(right[:-3]):  # 到倒数第三个 =
                pass







if __name__ == '__main__':
    ga = GrammarAnalyzer('./grammar_table.txt')
    for i in ga.grammar_table:
        print(i)
    ga.gen_firstvt_lastvt()
    for i in ga.grammar_table:
        print(i)
    a = ['a', 'b', 'c']
    print('index', a.index('a'))