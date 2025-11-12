from url_work import from_my_url
from reg_exe import create_login
import re
print("Если вы хотите сделать проверку на тандемность слова через файл — введите 1")
print("Если вы хотите сделать проверку на тандемность слова через ввод с консоли — введите 2")
print("Если вы хотите сделать проверку на тандемность слова через ввод с сайта — введите 3")
message = input("Введите выбор: ")

if message == "1": # Проверка через файл
    try:
        with open('text.txt', 'r', encoding='utf-8') as f:
            data = f.read().strip()

        print("Файл успешно считан\n")

        for re.match in create_login(data):
            # .group(0) — всё слово, .group(1) — повторяющаяся часть
            print(f"Найдено слово: {re.match.group(0)}")

    except FileNotFoundError:
        print("Ошибка: файл не найден.")

elif message == "2":# Проверка через консоль
        text = input("Введите текст: ")
        for i in create_login(text):
            print(i.group())

elif message == "3":# Проверка с сайта
    values = create_login(from_my_url('https://gist.github.com/Kan457/589b69ca0c16d69116487aeb92f2cb9d/raw'))
    results = [m.group(0) for m in values]
    print(results)

else:
    print("Некорректный ввод. Попробуйте заново")

if __name__ == "__main__":
    pass