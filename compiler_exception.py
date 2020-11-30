# @Author  : Edlison
# @Date    : 11/17/20 00:12

class CompilerException(Exception):
    # Compiler Exception.
    #
    # @Author  : Edlison
    # @Date    : 12/1/20 02:49
    def __init__(self, *args):
        self.args = args
        self.type = 'Compiler'
        self.msg = 'Default'

    def __str__(self):
        return '{}异常：{}.'.format(self.type, self.msg)


class WordAnalyseException(CompilerException):
    def __init__(self, msg):
        """
        Word Analyse Exception implement Compiler Exception.

        Args:
            msg(str): explanation for exception.

        Returns:

        @Author  : Edlison
        @Date    : 12/1/20 02:50
        """
        self.type = '词法分析'
        self.msg = msg


class GrammarAnalyseException(CompilerException):
    def __init__(self, msg):
        """
        Grammar Analyse Exception implement Compiler Exception.

        Args:
            msg(str): explanation for exception.

        Returns:

        @Author  : Edlison
        @Date    : 12/1/20 02:51
        """
        self.type = '语法分析'
        self.msg = msg


class MeaningAnalyseException(CompilerException):
    def __init__(self, msg):
        """
        Meaning Analyse Exception implement Compiler Exception.

        Args:
            msg(str): explanation for exception.

        Returns:

        @Author  : Edlison
        @Date    : 12/1/20 02:51
        """
        self.type = '语义分析'
        self.msg = msg