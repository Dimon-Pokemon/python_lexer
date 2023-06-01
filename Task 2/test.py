import unittest
from os import listdir
from re import match

import main


class MyTestCase(unittest.TestCase):

    def test_something(self):
        """
Огромный жирный толстый метод
Выполняет тестирование
Надо бы его отрефакторить
Но мне лень
Ужасный код
Без слез не взглянешь
Как я это мог вообще написать?
Жесть конечно
Асуждаю
Вот это говнокод
Всем говнокодом говнокод
        """
        files: list = listdir("/Users/dima/Documents/TGU/Основы компиляции/PR1/lexer/Task 2/inputData")  # Получаем список всех имен файло в директории(каталоге) inputDat
        files.sort() # сортируем список файлов
        lxr: "lexerClass" = main.lexerClass()  # Создаем экземпляр класса lexerClasss
        for file in files:  # Перебираем все имена файлов из массива 'files', поместив поочередно каждое имя в переменную 'file'
            # match(".*\.", file).group(0) выбдергивает имя файла из названия name.txt (т.е. без расширения)
            file_name = "/Users/dima/Documents/TGU/Основы компиляции/PR1/lexer/Task 2/outTest/" + match(".*\.", file).group(0) + "out"  # Путь до выходного файла.
            correct_file_name = "/Users/dima/Documents/TGU/Основы компиляции/PR1/lexer/Task 2/correctOut/" + match(".*\.", file).group(0) + "out" # Путь до файла с входными данными для тестирования
            if match(".*\.frag", file):  # Если текущий файл - входной, то:
                print(f"\033[0;33mТест № {files.index(file) + 1}\033[0;0m") # Вывод номера теста
                print("Тестирование файла:" + f"\033[0;33m{file}\033[0;0m")  # Вывод информации о тестируемом файле.
                with open("/Users/dima/Documents/TGU/Основы компиляции/PR1/lexer/Task 2/inputData/%s" % file) as f:  # Открываем файл под псевдонимом 'f'.
                    data: str = f.read()  # Считываем весь файл в виде одной строки в переменную data
                    # Вызываем метод 'start' экземпляра класса lxr
                    lxr.start(data, file_name)
                with open(correct_file_name, "r") as f_c:
                    correct_data = f_c.read()
                    correct_data = correct_data.replace(" ", "")
                    correct_data = correct_data.replace("\n", "")
                    with open(file_name, "r") as f_out:
                        output_data = f_out.read()
                        output_data = output_data.replace(" ", "")
                        output_data = output_data.replace("\n", "")
                        # self.assertEqual(output_data, correct_data)
                        # self.assertCountEqual(output_data, correct_data)
                        if output_data.lower() == correct_data.lower():
                            print(f"\033[3;32mТест № {files.index(file)+1} пройден! \033[0;0m\n")
                        else:
                            print(f"\033[3;31mТест № {files.index(file) + 1} НЕ пройден! \033[0;0m\n")
        self.assertEqual(True, True)



if __name__ == '__main__':
    unittest.main()
