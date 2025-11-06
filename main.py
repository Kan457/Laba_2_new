import unittest
from url_work import from_my_url
from file_work import from_my_file
from input_work import from_my_input
print("Если вы хотите сделать проверку на тандемность слова через файл — введите 1")
print("Если вы хотите сделать проверку на тандемность слова через ввод с консоли — введите 2")
print("Если вы хотите сделать проверку на тандемность слова через ввод с сайта — введите 3")
message = input("Введите выбор: ")

if message == "1": # Проверка через файл
    try:
        with open('testing_file.txt', 'r', encoding='utf-8') as f:
            data = [line.strip() for line in f.readlines()]
            from_my_file(data)
        print("Файл успешно считан ")


    except FileNotFoundError:
        print("Ошибка: файл не найден.")


    unittest.main()

elif message == "2":# Проверка через консоль

    text = input("Введите почту: ")
    data = text.split()
    from_my_input(data)

    unittest.main()

elif message == "3":# Проверка с сайта
    data = from_my_url('https://gist.github.com/Kan457/589b69ca0c16d69116487aeb92f2cb9d/raw')
    
    unittest.main()

else:
    print("Некорректный ввод. Попробу")

if __name__ == "__main__":
    pass