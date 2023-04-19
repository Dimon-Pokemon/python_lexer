from numpy import float128
import ply.lex as lex


class lexerClass:
    out_file: str = ""
    count_pos = 1  # Счетчик символов. Его время от времени будем сбрасывать
    last_line = 0  # Переменная для хранения номера прошлой строки. Если не совпадает, надо сбросить count
    len_last_token = 0
    file = ""
    '''
     Сохранение значения токена-числа, в изначальном виде. 
     Потому что при преобразовании к Double или Intупук число преобразуется в 10 с.с. 
     и представляется в десятичном виде.
     Например 0x0 преобразуется в 0, 1.2E2 в 120.0
     '''
    first_value_digit = 0

    def __init__(self, out_file="result.out"):
        self.out_file = out_file

    def set_out_file(self, out_file: str):
        self.out_file = out_file

    """
    LESS_CHAR           - <
    LESS_OR_EQUALS_CHAR - <=
    MORE_CHAR           - >
    MORE_OR_EQUALS_CHAR - >=
    ASSIGNMENT          - =
    EQUALS              - ==
    """
    tokens = ["DOUBLE_NUMBER", 'BOOLCONST', 'T_ERROR_LONG_IDENTIFIER', 'IDENTIFIER', "SINGLE_COMMENT",
              "MULTILINE_COMMENT", 'NUMBER', 'PLUS',
              'MINUS', 'TIMES', 'NOT_EQUALS', 'AND', 'OR', 'SCREAM',
              'SEMICOLON', 'COMMA', 'POINT', 'OPEN_SQUARE_BRACKET',
              'CLOSE_SQUARE_BRACKET', 'OPEN_ROUND_BRACKET',
              'CLOSE_ROUND_BRACKET', 'OPEN_BRACE', 'CLOSE_BRACE',
              'DOUBLE_SQUARE_BRACKETS', 'DOUBLE_ROUND_BRACKETS',
              'DOUBLE_BRACES', 'DIVIDE', 'EQUALS', 'LPAREN', 'RPAREN',
              "PERCENT", "LESS_CHAR", "LESS_OR_EQUALS_CHAR",
              "MORE_CHAR", "MORE_OR_EQUALS_CHAR", "ASSIGNMENT",
              "CONSTSTRING", "MULTILINE_NON_CLOSED_COMMENT"]

    # Tokens

    def t_DOUBLE_NUMBER(self, t):
        r'((0([1][0-9]{0,18})?)|([1-9][0-9]{0,19}))\.[0-9]{0,100}((E|e)(\+|-)?([[0-9]{1,4}))?'
        try:
            self.first_value_digit = t.value
            t.value = float128(t.value)
        except ValueError:
            print("Double value too large ", t.value)
            t.value = 0
        return t

    def t_NUMBER(self, t):
        r'(0(x|X)[0-9a-fA-F]+)|(\d+)'
        try:
            self.first_value_digit = t.value
            t.value = int(t.value)
        except ValueError:
            # Костыльное решение. Связанное с возможностью записи числа в 16 системе счисления
            try:
                t.value = int(t.value, 16)
                return t
            except ValueError:
                print(f"Integer value too large {t.value}")
                t.value = 0
            print(f"Integer value too large {t.value}")
            t.value = 0
        return t

    def T_MULTILINE_NON_CLOSED_COMMENT(self, t):
        r'\/\*.+'
        raise RuntimeError("Комментарий не закрыт!")

    def T_ERROR_LONG_IDENTIFIER(self, t):
        r'([a-zA-Z_][a-zA-Z0-9_]{30,100}){1,100}?'
        self.file.writelines([f"\n*** Error line {self.last_line}\n", f"*** Identifier too long: \"{t.value[0]}\"\n"])
        t.lexer.skip(1)

    def t_SCREAM(self, t):
        r'!'
        return t

    def t_SEMICOLON(self, t):
        r';'
        return t

    def t_COMMA(self, t):
        r','
        return t

    def t_PLUS(self, t):
        r"\+"
        return t

    def t_POINT(self, t):
        r'\.'
        return t

    def t_MINUS(self, t):
        r"-"
        return t

    def t_TIMES(self, t):
        r"\*"
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

    def t_MULTILINE_COMMENT(self, t):
        r'\/\*(.|\n)*?\*\/'

    def t_SINGLE_COMMENT(self, t):
        r'//.*\n?'

    t_ignore = " \r\t\f"

    def t_newline(self, t):
        r'\n+'
        # self.last_line = t.lexer.lineno
        t.lexer.lineno += t.value.count("\n")
        self.count_pos = 1

    def t_error(self, t):
        # with open(self.out_file, "a") as f:
        # print(f"\n*** Error line {self.last_line}\n", file=self.file)
        self.file.writelines([f"\n*** Error line {t.lexer.lineno}.\n", f"*** Unrecognized char: '{t.value[0]}'\n"])
        t.lexer.skip(1)

    def t_IDENTIFIER(self, t):
        r'[a-zA-Z_]([a-zA-Z0-9_]{1,29})?'  # Имя переменной. Длина не более 31 символа.
        t.type = self.reserved.get(t.value, 'IDENTIFIER')
        return t

    reserved = {
        'void': 'VOID',
        'double': 'DOUBLE',
        'int': 'INT',
        'bool': 'BOOL',
        'string': 'STRING',
        'true': 'BOOLCONST',
        'false': 'BOOLCONST',
        'class': 'CLASS',
        'interface': 'INTERFACE',
        'null': 'NULL',
        'this': 'THIS',
        'extends': 'EXTENDS',
        'implements': 'IMPLEMENTS',
        'for': 'FOR',
        'while': 'WHILE',
        'if': 'IF',
        'else': 'ELSE',
        'return': 'RETURN',
        'break': 'BREAK',
        'new': 'NEW',
        'NewArray': 'NEWARRAY',
        'Print': 'PRINT',
        'ReadInteger': 'READINTEGER',
        'ReadLine': 'READLINE'
    }

    tokens += list(reserved.values())

    #t_MULTILINE_COMMENT = r'\/\*(.|\n)*?\*\/'
    #t_SINGLE_COMMENT = r'//.*\n?'
    t_DOUBLE_SQUARE_BRACKETS = r'\[\]'
    t_DOUBLE_ROUND_BRACKETS = r'\(\)'
    t_DOUBLE_BRACES = r'\{\}'
    t_AND = r'\&\&'
    t_OR = r'\|\|'
    t_CONSTSTRING = r'"([^"])*"'
    t_EQUALS = r"=="
    t_NOT_EQUALS = r'!='
    t_LESS_OR_EQUALS_CHAR = r'<='
    t_MORE_OR_EQUALS_CHAR = r'>='
    t_ASSIGNMENT = r'='
    t_MORE_CHAR = r'>'
    t_LESS_CHAR = r'<'
    t_DIVIDE = r'/'

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
                # self.count_pos += len(token["value"])
                if self.last_line == token["lineno"]:
                    self.count_pos += self.len_last_token
                else:
                    self.count_pos = 1
                if str(token["type"]) in ("NUMBER", "DOUBLE_NUMBER"):
                    self.file.write("{0} line {1} cols {2}-{3} is {4} (value = {5})\n".format(self.first_value_digit,
                                                                                              str(token["lineno"]),
                                                                                              self.count_pos,
                                                                                              str(len(
                                                                                                  str(token[
                                                                                                          "value"])) + self.count_pos - 1),
                                                                                              "T_" + str(token["type"]),
                                                                                              str(token["value"])))
                else:
                    self.file.write(
                        "{0} line {1} cols {2}-{3} is {4}\n".format(str(token["value"]), str(token["lineno"]),
                                                                    self.count_pos,
                                                                    str(len(
                                                                        str(token[
                                                                                "value"])) + self.count_pos - 1),
                                                                    "T_" + str(token["type"])))
                self.len_last_token = len(str(token["value"]))
                self.last_line = token["lineno"]


if __name__ == "__main__":
    data = '123+345*(45-33)/233'
    lxr = lexerClass()
    lxr.start(data)
    ;
