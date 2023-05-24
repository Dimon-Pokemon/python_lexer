# coding=utf8

from parser import build_tree

data = '''
2.25
2.77 lexer
'''

result = build_tree(data)
print( result )
