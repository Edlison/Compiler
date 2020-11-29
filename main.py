# @Author  : Edlison
# @Date    : 11/30/20 02:00

from word_analysis import WordAnalyzer
from grammar_analysis import GrammarAnalyzer

WA = WordAnalyzer(table='./words_table.txt', input='./input.txt')
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
