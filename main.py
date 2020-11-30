# @Author  : Edlison
# @Date    : 11/30/20 02:00

from word_analysis import WordAnalyzer
from grammar_analysis import GrammarAnalyzer
from meaning_analysis import MeaningAnalyzer


class Compiler:
    def __init__(self, input, words_table, grammar_table, use_meaning=False):
        self.word_analyzer = WordAnalyzer(input=input, table=words_table)
        token_stack = self._get_token_stack()
        if use_meaning:
            self.meaning_analyzer = MeaningAnalyzer(grammar_table_path=grammar_table)
            self.meaning_analyzer.analyse(token_stack)
        else:
            self.grammar_analyzer = GrammarAnalyzer(grammar_table_path=grammar_table)
            self.grammar_analyzer.analyse(token_stack)

    def _get_token_stack(self):
        word_token = self.word_analyzer.word_token
        res = []
        for each in word_token:
            if 39 <= each.code <= 43:
                res.append('id')
                continue
            res.append(each.name)
        return res


Compiler(input='./data/input_1.txt', words_table='./data/words_table.txt', grammar_table='./data/grammar_table_current.txt')
Compiler(input='./data/input_2.txt', words_table='./data/words_table.txt', grammar_table='./data/grammar_table_min.txt', use_meaning=True)