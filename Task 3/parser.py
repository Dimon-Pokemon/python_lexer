# coding=utf8

import lexer as lex
import ply.yacc as yacc


class Node:

    def parts_str(self):
        st = []
        for part in self.parts:
            st.append(str(part))
        return "\n".join(st)

    def __repr__(self):
        return self.type + ":\n\t" + self.parts_str().replace("\n", "\n\t")

    def add_parts(self, parts):
        self.parts += parts
        return self

    def __init__(self, type, parts):
        self.type = type
        self.parts = parts


class Parser:

    def p_init_variable(p):
        """
         variable : type identifier assignment boolconst
              | type identifier assignment double_number
              | type identifier assignment number
              | type identifier assignment conststring
        """
        if p[0] == 'BOOL':
            p[0] = Node('IDENTIFIER_BOOL', [p[1]])
        elif p[0] == 'DOUBLE':
            p[0] = Node('IDENTIFIER_DOUBLE', [p[1]])
        elif p[0] == 'INT':
            p[0] = Node('IDENTIFIER_INT', [p[1]])
        elif p[0] == 'STRING':
            p[0] = Node('IDENTIFIER_INT', [p[1]])
        else:
            p[0] = Node("INIT_VARIABLE", [p[1], p[2], p[3], p[4]])

    def p_assignment(p):
        """
        assignment : ASSIGNMENT
        """
        p[0] = Node("ASSIGNMENT", [p[1]])

    def p_boolconst(p):
        """
         boolconst : BOOLCONST
        """
        p[0] = Node("BOOLCONST", [p[1]])

    def p_double_number(p):
        """
         double_number : DOUBLE_NUMBER
        """
        p[0] = Node("DOUBLE_NUMBER", [p[1]])

    def p_number(p):
        """
         number : NUMBER
        """
        p[0] = Node("NUMBER", [p[1]])

    def p_conststring(p):
        """
         conststring : CONSTSTRING
        """
        p[0] = Node("CONSTSTRING", [p[1]])

    def p_variable_declaration(p):
        """
        var_dec : type identifier
        """
        p[0] = Node("VARIABLE_DECLARATION", [p[1], p[2]])

    def p_identifier(p):
        """
        identifier : IDENTIFIER
        """
        p[0] = Node("IDENTIFIER", [p[1]])

    def p_type(p):
        """
        type : BOOL
             | INT
             | STRING
             | DOUBLE
        """
        p[0] = Node("TYPE", [p[1]])

    def p_string(p):
        """
        string : CONSTSTRING
        """
        print("It is work")
        p[0] = Node("STRING", [p[1]])



    lexer = None
    tokens = lex.lexerClass.tokens
    print(tokens)
    reserved = lex.lexerClass.reserved


    def __init__(self, code):
        self.lexer = lex.lexerClass()
        self.lexer.start(code)

    def build_tree(self, code):
        return self.parser.parse(code)

    def p_error(p):
        print ( 'Unexpected token:', p )

    parser = yacc.yacc()


