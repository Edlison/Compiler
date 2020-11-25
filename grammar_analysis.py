# @Author  : Edlison
# @Date    : 11/17/20 00:11
import os
from typing import List, Dict, Set
from compiler_exception import GrammarAnalyseException


# TODO 1.analyse stack 生成产生式
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

        for each in right.split(' '):
            if each.isupper():
                self.non_terminal.append(each)
            else:
                self.terminal.append(each)

    def __str__(self):
        return 'ID: {} \t Left: {} \t Right: {} \n end: {} \n not_end: {} \n'.format(
            self.id, self.left, self.right, self.terminal, self.non_terminal)


class PriorityTable:
    def __init__(self):
        self.terminal = []
        self.firstvt: (str, set) = {}
        self.lastvt: (str, set) = {}
        self.relation = {0: 'ni', 1: '=', 2: '<', 3: '>'}

    def is_in_terminal(self, s):
        for each in self.terminal:
            if s == each:
                return True
        return False


class GrammarAnalyzer:
    def __init__(self, grammar_table_path):
        self.text = ''
        self.grammar_table: List[Grammar] = []
        self.priority_table: PriorityTable = PriorityTable()

        self._load_grammar_table(grammar_table_path)

    def _load_grammar_table(self, path):
        if not os.path.exists(path):
            raise GrammarAnalyseException('文法表不存在')
        with open(path) as f:
            grammar_list = f.read()
        grammar_list = eval(grammar_list)

        for each in grammar_list:
            self.grammar_table.append(Grammar(each[0], each[1], each[2]))

    def gen_firstvt_lastvt(self):
        # 生成priority_table独立的firstvt lastvt
        for each_grammar in self.grammar_table:
            if not self.priority_table.firstvt.get(each_grammar.left) and not self.priority_table.lastvt.get(
                    (each_grammar.left)):
                self.priority_table.firstvt[each_grammar.left] = set()
                self.priority_table.lastvt[each_grammar.left] = set()

        # 考虑只是终结符的情况
        for each_grammar in self.grammar_table:
            right = each_grammar.right.split(' ')
            # firstvt
            if not right[0].isupper() and right[0] is not '?':
                self.priority_table.firstvt[each_grammar.left].add(right[0])
            else:
                if len(right) > 1:
                    if not right[1].isupper():
                        self.priority_table.firstvt[each_grammar.left].add(right[1])
            # lastvt
            last = len(right) - 1
            if not right[last].isupper() and right[last] is not '?':
                self.priority_table.lastvt[each_grammar.left].add((right[last]))
            else:
                if len(right) > 1:
                    if not right[last - 1].isupper():
                        self.priority_table.lastvt[each_grammar.left].add(right[last - 1])

        # 考虑非终结符开头结尾的情况
        for each_grammar in reversed(self.grammar_table):
            if each_grammar.right[0].isupper():
                self.priority_table.firstvt[each_grammar.left].update(self.priority_table.firstvt[each_grammar.right[0]])
            if each_grammar.right[-1].isupper():
                self.priority_table.lastvt[each_grammar.left].update(self.priority_table.lastvt[each_grammar.right[-1]])

    def gen_priority_table(self):
        # Table拿到所有终结符
        for each_grammar in self.grammar_table:
            terminal = each_grammar.terminal
            for each_terminal in terminal:
                if not self.priority_table.is_in_terminal(each_terminal) and each_terminal is not '?':
                    self.priority_table.terminal.append(each_terminal)
        row_col = len(self.priority_table.terminal)
        table = [[self.priority_table.relation[0] for _ in range(row_col)] for _ in range(row_col)]

        for each_grammar in self.grammar_table:
            right = each_grammar.right.split(' ')
            for i, _ in enumerate(right[:-1]):
                if not right[i].isupper() and not right[i + 1].isupper():
                    row = self.priority_table.terminal.index(right[i])
                    col = self.priority_table.terminal.index(right[i + 1])
                    table[row][col] = self.priority_table.relation[1]  # 1: '='
                if i < len(right) - 2 and not right[i].isupper() and not right[i + 2].isupper():
                    row = self.priority_table.terminal.index(right[i])
                    col = self.priority_table.terminal.index(right[i + 2])
                    table[row][col] = self.priority_table.relation[1]  # 1: '='
                if not right[i].isupper() and right[i + 1].isupper():
                    row = self.priority_table.terminal.index(right[i])
                    for each_firstvt in self.priority_table.firstvt[right[i + 1]]:
                        col = self.priority_table.terminal.index(each_firstvt)
                        table[row][col] = self.priority_table.relation[2]  # 2: '<'
                if right[i].isupper() and not right[i + 1].isupper():
                    col = self.priority_table.terminal.index(right[i + 1])
                    for each_lastvt in self.priority_table.lastvt[right[i]]:
                        row = self.priority_table.terminal.index(each_lastvt)
                        table[row][col] = self.priority_table.relation[3]  # 3: '>'
                # raise GrammarAnalyseException('优先表无此关系')
        self.table = table


if __name__ == '__main__':
    ga = GrammarAnalyzer('grammar_table_full.txt')
    for i in ga.grammar_table:
        print(i)
    ga.gen_firstvt_lastvt()

    print('first', ga.priority_table.firstvt)
    print('last', ga.priority_table.lastvt)

    ga.gen_priority_table()

    for i in ga.priority_table.terminal:
        print('\t' + i, end='')
    print()
    for i, each in enumerate(ga.table):
        print(ga.priority_table.terminal[i] + '\t', end='')
        for j in each:
            print(j + '\t', end='')
        print()


