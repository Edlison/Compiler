# @Author  : Edlison
# @Date    : 11/17/20 00:12

class CompilerException(Exception):
    def __init__(self, *args):
        self.args = args
        self.type = 'Compiler'
        self.msg = 'Default'

    def __str__(self):
        return '{}异常：{}.'.format(self.type, self.msg)


class WordAnalyseException(CompilerException):
    def __init__(self, msg):
        self.type = '词法分析'
        self.msg = msg


class GrammarAnalyseException(CompilerException):
    def __init__(self, msg):
        self.type = '语法分析'
        self.msg = msg

