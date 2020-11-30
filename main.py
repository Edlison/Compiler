# @Author  : Edlison
# @Date    : 11/30/20 02:00

# TODO 整理类之间的调用

from word_analysis import WordAnalyzer
from grammar_analysis import GrammarAnalyzer
from meaning_analysis import GrammarAnalyzer as MGA


def using_grammar_ana():
    WA = WordAnalyzer(table='./words_table.txt', input='./input_1.txt')
    GA = GrammarAnalyzer(grammar_table_path='grammar_table_current.txt')
    temp = WA.word_token
    word_token = []
    for each in temp:
        if 39 <= each.code <= 43:
            word_token.append('id')
            continue
        word_token.append(each.name)
    print(word_token)
    GA._analyse(word_token)


def using_meaning_ana():
    WA = WordAnalyzer(table='./words_table.txt', input='./input_2.txt')
    m = MGA('grammar_table_min.txt')

    temp = WA.word_token
    word_token = []
    for each in temp:
        if 39 <= each.code <= 43:
            word_token.append('id')
            continue
        word_token.append(each.name)
    print(word_token)
    m._analyse(word_token)


using_meaning_ana()
