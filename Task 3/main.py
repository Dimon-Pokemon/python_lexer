# coding=utf8

from parser import Parser





if __name__ == "__main__":
    # data = '''
    # int p = gjklrtjglkrtdj
    # '''

    # data = """
    # int p = 25
    # """

    data = """
    int ItIsInteger = 125
    """

    parser = Parser(data)
    parser.build_tree(data)
    result = parser.build_tree(data)

    print(result)
