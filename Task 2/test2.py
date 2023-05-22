from os import listdir

def test():
    files: list = listdir("inputData")  # Получаем список всех имен файлов в директории(каталоге) inputData
    files.sort()  # сортируем список файлов
    for fileName in files: # перебираем номера имен файлов в списке files
        with open(fileName, "a") as file:
            start()

