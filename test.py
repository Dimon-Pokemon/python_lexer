import unittest
from os import listdir
from re import match

import main2


class MyTestCase(unittest.TestCase):

    def test_something(self):
        files: list = listdir("inputData")  # Получаем список всех имен файло в директории(каталоге) inputDat
        files.sort()
        lxr: "lexerClass" = main2.lexerClass()  # Создаем экземпляр класса lexerClasss
        for file in files:  # Перебираем все имена файлов из массива 'files', поместив поочередно каждое имя в 'file'
            file_name = "outTest/" + match(".*\.", file).group(0) + "out"  # Путь до выходного файла.
            correct_file_name = "correctOut/" + match(".*\.", file).group(0) + "out"
            if match(".*\.frag", file):  # Если текущий файл - входной, то:
                print("Тестирование файла:" + f"\033[0;33m{file}\033[0;0m")  # Вывод информации о тестируемом файле.
                with open("inputData/%s" % file) as f:  # Открываем файл под псевдонимом 'f'.
                    data: str = f.read()  # Считываем весь файл в виде одной строки в переменную data
                    # Вызываем метод 'start' экземпляра класса lxr
                    lxr.start(data, file_name)
                with open(correct_file_name, "r") as f_c:
                    correct_data = f_c.read()
                    correct_data = correct_data.replace(" ", "")
                    with open(file_name, "r") as f_out:
                        output_data = f_out.read()
                        output_data = output_data.replace(" ", "")
                        self.assertEqual(output_data, correct_data)
                        print(f"\033[3;32mТест № {files.index(file)+1} пройден! \033[0;0m")

        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
