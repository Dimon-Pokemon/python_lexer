import unittest
from os import listdir
from re import match

import main2


class MyTestCase(unittest.TestCase):

    def test_something(self):
        files: list = listdir("inputData")  # Получаем список всех имен файло в директории(каталоге) inputData
        lxr: "lexerClass" = main2.lexerClass()  # Создаем экземпляр класса lexerClasss
        for file in files:  # Перебираем все имена файлов из массива 'files', поместив поочередно каждое имя в 'file'
            file_name = "outTest/" + match(".*\.", file).group(0) + "out"  # Путь до выходного файла.
            if match(".*\.frag", file):  # Если текущий файл - входной, то:
                print("Тестирование файла:" + file)  # Вывод информации о тестируемом файле.
                with open("inputData/%s" % file) as f:  # Открываем файл под псевдонимом 'f'.
                    data: str = f.read()  # Считываем весь файл в виде одной строки в переменную data
                    # Вызываем метод 'start' экземпляра класса lxr
                    lxr.start(data, file_name)
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
