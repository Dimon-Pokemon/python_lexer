from numpy import float128
from os import listdir
import ply.lex as lex
from ply.lex import TOKEN
import re


class lexerClass:
    out_file: str = ""
    count_pos = 1  # Счетчик символов. Его время от времени будем сбрасывать
    last_line = 1  # Переменная для хранения номера прошлой строки. Если не совпадает, надо сбросить count
    file = "";

    def __init__(self, out_file="result.out"):
        self.out_file = out_file

    def set_out_file(self, out_file: str):
        self.out_file = out_file

    """
    LESS_CHAR         - <
    LESS_OR_EQUALS_CHAR - <=
    MORE_CHAR         - >
    MORE_OR_EQUALS_CHAR - >=
    ASSIGNMENT       - =
    EQUALS           - ==
    """
    tokens = ('IDENTIFIER', "SINGLE_COMMENT", "MULTILINE_COMMENT",
              'NUMBER', "DOUBLE_NUMBER", 'PLUS',
              'MINUS', 'TIMES', 'NOT_EQUALS', 'AND', 'OR', 'SCREAM',
              'SEMICOLON', 'COMMA', 'POINT', 'OPEN_SQUARE_BRACKET',
              'CLOSE_SQUARE_BRACKET', 'OPEN_ROUND_BRACKET',
              'CLOSE_ROUND_BRACKET', 'OPEN_BRACE', 'CLOSE_BRACE',
              'DOUBLE_SQUARE_BRACKETS', 'DOUBLE_ROUND_BRACKETS',
              'DOUBLE_BRACES', 'DIVIDE', 'EQUALS', 'LPAREN', 'RPAREN',
              "PERCENT", "LESS_CHAR", "LESS_OR_EQUALS_CHAR",
              "MORE_CHAR", "MORE_OR_EQUALS_CHAR", "ASSIGNMENT",
              "VOID", "INT", "DOUBLE", "BOOL", "STRING", "CONSTSTRING",
              "CLASS", "INTERFACE", "NULL", "THIS", "EXTENDS",
              "IMPLEMENTS", "FOR", "WHILE", "IF", "ELSE",
              "RETURN", "BREAK", "NEW", "NEWARRAY", "PRINT",
              "READINTEGER", "READLINE", "MULTILINE_NON_CLOSED_COMMENT")

    # Tokens
    t_SINGLE_COMMENT = r'//.*\n?'
    t_MULTILINE_COMMENT = r'\/\*(.|\n)*?\*\/'
    t_EQUALS = r"=="
    t_NOT_EQUALS = r'!='
    t_AND = r'\&\&'
    t_OR = r'\|\|'
    t_LESS_OR_EQUALS_CHAR = r'<='
    t_MORE_OR_EQUALS_CHAR = r'>='
    t_DOUBLE_SQUARE_BRACKETS = r'\[\]'
    t_DOUBLE_ROUND_BRACKETS = r'\(\)'
    t_DOUBLE_BRACES = r'\{\}'
    t_VOID = r'void'
    t_DOUBLE = r'Double'
    t_INT = r'Int'
    t_BOOL = r'Bool'
    t_STRING = r'String'
    t_CONSTSTRING = r'".*"'
    t_CLASS = r'class'
    t_INTERFACE = r'interface'
    t_NULL = r'null'
    t_THIS = r'this'
    t_EXTENDS = r'extends'
    t_IMPLEMENTS = r'implements'
    t_FOR = r'for'
    t_WHILE = r'while'
    t_IF = r'if'
    t_ELSE = r'else'
    t_RETURN = r'return'
    t_BREAK = r'break'
    t_NEW = r'new'
    t_NEWARRAY = r'NewArray'
    t_PRINT = r'Print'
    t_READINTEGER = r'ReadInteger'
    t_READLINE = r'ReadLine'
    t_IDENTIFIER = r'[a-zA-Z_]([a-zA-Z0-9_]{1,30})?'  # Имя переменной. Длина не более 31 символа.

    def T_MULTILINE_NON_CLOSED_COMMENT(self, t):
        r'\/\*.+'
        raise RuntimeError("Комментарий не закрыйт!")

    def t_SCREAM(self, t):
        r'!'
        return t

    def t_SEMICOLON(self, t):
        r';'
        return t

    def t_COMMA(self, t):
        r','
        return t

    def t_POINT(self, t):
        r'\.'
        return t

    def t_NUMBER(self, t):
        r'\d+'
        try:
            t.value = int(t.value)
        except ValueError:
            print("Integer value too large %d" % t.value)
            t.value = 0
        return t

    def t_DOUBLE_NUMBER(self, t):
        r'[0-9]{1,20}\.[0-9]{0,100}E|e(\+|-)([1-9][0-9]?){1,2}'
        try:
            t.value = float128(t.value)
        except ValueError:
            print("Double value too large ", t.value)
            t.value = 0
        return t

    def t_PLUS(self, t):
        r"\+"
        return t

    def t_MINUS(self, t):
        r"-"
        return t

    def t_TIMES(self, t):
        r"\*"
        return t

    """
    Итак, возникла проблема, связанная с тем, что регулярное выражение вида r'/'
    срабатывает на многострочные комментарии, т.е. строку '/**/' лексер воспринимает как два деления и умножения.
    Решение этой проблемы я наше в том, что указать, что после косой черты не должен идти символ умножения,
    т.е. '/[^\*]', где 
    '/' - знак деления, 
    [^\*] - класс символов, которые могут быть на следующей позиции после предыдущего знака '/', т.е.
    в данном случае может быть любой символ, кроме '*', потому что '/*' обозначает начало многострочного коммента. 
    Но тогда появляется побочный эффект - т.к. в регулярке указаны два символа, то соответственно не получается применить функцию
    ord, т.к. она работает с одним символом. Но мы точно знаем, что первый символ - это символ косой черты, а следователньо можем
    взять первый символ строки [0]. Это и есть костыль.   
    """

    def t_DIVIDE(self, t):
        r'/'  # /[^\*\/]
        # r"((%s)|(\d))\/((%s)|(\d))"%(t_IDENTIFIER, t_IDENTIFIER)
        # "(([a - zA - Z_]([a - zA - Z0 - 9_]{1, 30})?) | (\d))\ / (([a - zA - Z_]([a - zA - Z0 - 9_]{1, 30})?) | (\d))"
        return t

    def t_ASSIGNMENT(self, t):
        r"="
        return t

    def t_OPEN_ROUND_BRACKET(self, t):
        r"\("
        return t

    def t_CLOSE_ROUND_BRACKET(self, t):
        r"\)"
        return t

    def t_OPEN_SQUARE_BRACKET(self, t):
        r'\['
        return t

    def t_CLOSE_SQUARE_BRACKET(self, t):
        r'\]'
        return t

    def t_OPEN_BRACE(self, t):
        r'\{'
        return t

    def t_CLOSE_BRACE(self, t):
        r'\}'
        return t

    def t_LESS_CHAR(self, t):
        r"<"
        return t

    def t_MORE_CHAR(self, t):
        r">"
        return t

    t_ignore = " \r\t\f"

    def t_newline(self, t):
        r'\n+'
        self.last_line = t.lexer.lineno
        t.lexer.lineno += t.value.count("\n")
        self.count_pos += 1

    def t_error(self, t):
        #with open(self.out_file, "a") as f:
        #print(f"\n*** Error line {self.last_line}\n", file=self.file)
        self.file.writelines([f"\n*** Error line {self.last_line}\n", f"*** Unrecognized char: '{t.value[0]}'\n"])
        t.lexer.skip(1)

    def start(self, data: str, out_file="outTest/result.txt"):
        self.out_file = out_file
        lexer = lex.lex(object=self)
        lexer.input(data)
        with open(self.out_file, "w") as self.file:
            for i in range(len(data)):
                tok = lexer.token()
                if not tok:
                    break
                # print(tok)
                token = tok.__dict__
                if token["lineno"] == self.last_line and i != 0:
                    self.count_pos += len(str(token["value"]))
                else:
                    self.count_pos = 1
                self.file.write("{0} line {1} cols {2}-{3} is {4}\n".format(str(token["value"]), str(token["lineno"]),
                                                                       str(self.count_pos),
                                                                       str(len(str(token["value"]))+self.count_pos-1),
                                                                       "T_"+str(token["type"])))

                self.last_line = token["lineno"]
            self.last_line = 1
            self.count_pos = 1


if __name__ == "__main__":
    data = '123+345*(45-33)/233'
    lxr = lexerClass()
    lxr.start(data)
