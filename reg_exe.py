import re

valid = re.compile(r'([a-zA-Zа-яА-Я]+)\1')

def create_login(text):
    return re.finditer(valid,text)

if __name__ == "__main__":
    pass