# @Author  : Edlison
# @Date    : 11/16/20 15:24
import os
from compiler_exception import WordAnalyseException


# Token表
class WordToken:
    def __init__(self, index: int, name: str, code: int, addr=0):
        """
        初始化词表

        Args:
            index: 编号
            name: 名字
            code: 编号
            addr: 在符号表中的位置（如果不是标识符或常数则为0）

        Returns:

        @Author  : Edlison
        @Date    : 11/16/20 20:13
        """
        self.index = index
        self.name = name
        self.code = code
        self.addr = addr

    def __str__(self):
        return 'index: {} \t name: {} \t code: {} \t addr: {}'.format(self.index, self.name, self.code, self.addr)


# 符号表
class WordSymbol(object):
    def __init__(self, index: int, name: str, type: int):
        """
        初始化符号表

        Args:
            index: 编号
            name: 名字
            type: 类型（0标识符，1常数）

        Returns:

        @Author  : Edlison
        @Date    : 11/16/20 20:14
        """
        self.index = index
        self.name = name
        self.type = type

    def __str__(self):
        return 'index: {} \t name: {} \t type: {}'.format(self.index, self.name, '标识符' if self.type == 0 else '常数')


class WordAnalyzer:
    def __init__(self, table, input):
        self.word_token = []
        self.word_symbol = []
        self.text = ''
        self.table = {}

        self._load_table(table)
        self._load_input(input)
        self._analyse()

    def _load_input(self, path):
        if not os.path.exists(path):
            raise WordAnalyseException('文件不存在')
        with open(path) as f:
            text = f.read()
        self.text = text

    def _load_table(self, path):
        if not os.path.exists(path):
            raise WordAnalyseException('文件不存在')
        with open(path) as f:
            table = f.read()
        table.strip()
        self.table = eval(table)

    def _is_keyword(self, s) -> bool:
        if not self.table.get(s):
            return False
        if 0 <= self.table[s] < 25:
            return True
        else:
            return False

    def _is_op(self, s):
        if not self.table.get(s):
            return False
        if 24 < self.table[s] < 39:
            return True
        else:
            return False

    def _is_delimiter(self, s):
        if not self.table.get(s):
            return False
        if 43 < self.table[s] < 55:
            return True
        else:
            return False

    def _is_integer(self, s):
        point_num = 0
        for ch in s:
            if ch == '.':
                point_num += 1
            if point_num is 0 and ('A' <= ch <= 'Z' or 'a' <= ch <= 'z'):
                raise WordAnalyseException('常数中出现字母')
            if point_num is 1 and ('A' <= ch <= 'Z' or 'a' <= ch <= 'z'):
                raise WordAnalyseException('常数的小数部分出现字母')
            if point_num is 2:
                raise WordAnalyseException('出现两个小数点')
        if point_num == 0:
            return True
        else:
            return False

    def _get_code(self, s):
        if self.table.get(s):
            return self.table[s]

    def _is_exist(self, s):
        for item in self.word_symbol:
            if item.name == s:
                return True
        return False

    def _get_addr(self, s):
        for item in self.word_symbol:
            if item.name == s:
                return item.index
        raise WordAnalyseException('未在常数表中出现')

    def _analyse(self):
        text_in_line = self.text.split('\n')
        for line in text_in_line:
            i = 0
            while i < len(line):
                if line[i] != ' ':  # 字符不为空时继续
                    word = ''  # 初始化当前word
                    if 'A' <= line[i] <= 'Z' or 'a' <= line[i] <= 'z':  # word 以 字母开头
                        while 'A' <= line[i] <= 'Z' or 'a' <= line[i] <= 'z' or '0' <= line[i] <= '9':
                            word += line[i]
                            i += 1
                        if self._is_keyword(word):  # 判断是不是关键字 不是的话只能是标识符
                            self.word_token.append(WordToken(len(self.word_token), word, self._get_code(word)))
                        else:  # 是标识符
                            if not self._is_exist(word):  # 标识符表中没有的话加入
                                self.word_symbol.append(WordSymbol(len(self.word_symbol), word, 0))
                            self.word_token.append(WordToken(len(self.word_token), word, self._get_code('id'), self._get_addr(word)))
                    elif '0' <= line[i] <= '9':  # word 以 数字开头
                        while '0' <= line[i] <= '9' or line[i] == '.' or 'A' <= line[i] <= 'Z' or 'a' <= line[i] <= 'z':
                            word += line[i]
                            i += 1
                        if self._is_integer(word):  # 整数
                            if not self._is_exist(word):
                                self.word_symbol.append(WordSymbol(len(self.word_symbol), word, self._get_code(1)))
                            self.word_token.append(WordToken(len(self.word_token), word, self._get_code('整型'), self._get_addr(word)))
                        else:  # 小数
                            if not self._is_exist(word):
                                self.word_symbol.append(WordSymbol(len(self.word_symbol), word, self._get_code(1)))
                            self.word_token.append(WordToken(len(self.word_token), word, self._get_code('实型'), self._get_addr(word)))
                    else:  # word 以 字符开头
                        word += line[i]
                        word_plus = word
                        if i+1 < len(line):
                            word_plus += line[i+1]
                        i += 1
                        if self._is_op(word):
                            self.word_token.append(WordToken(len(self.word_token), word, self._get_code(word)))
                        elif self._is_op(word_plus):
                            i += 1
                            self.word_token.append(WordToken(len(self.word_token), word, self._get_code(word_plus)))
                        elif self._is_delimiter(word):
                            self.word_token.append(WordToken(len(self.word_token), word, self._get_code(word)))
                        elif self._is_delimiter(word_plus):
                            i += 1
                            self.word_token.append(WordToken(len(self.word_token), word, self._get_code(word_plus)))
                        else:
                            raise WordAnalyseException('非法字符')
                else:  # 字符为空时直接跳过
                    i += 1
    def show(self):
        print('Input text:\n', self.text)
        print('\nWord Token')
        for item in self.word_token:
            print(item)
        print('\nWord Symbol')
        for item in self.word_symbol:
            print(item)


if __name__ == '__main__':
    wa = WordAnalyzer(table='./words_table.txt', input='./input.txt')
    wa.show()
