import unittest
from reg_exe import create_login
from url_work import from_my_url

#from_my_url
class TestFromMyUrl(unittest.TestCase):
    #Проверяет, что функция возвращает строку (если URL доступен)
    def test_real_url(self):
        url = "https://gist.github.com/Kan457/589b69ca0c16d69116487aeb92f2cb9d/raw"
        result = from_my_url(url)
        self.assertTrue(isinstance(result, (str, type(None))))

    #Проверяет обработку несуществующего URL
    def test_invalid_url(self):
            url = "https://thisurldefinitelydoesnotexist12345.com/"
            result = from_my_url(url)
            self.assertIsNone(result)

#create_login
class TestTandemRepeats(unittest.TestCase):
    #проверка простых повторений
    def test_finds_simple_repeats(self):
        text = "abcabc testtest домдом"
        results = [m.group(0) for m in create_login(text)]
        self.assertEqual(len(results), 3)
        self.assertIn("abcabc", results)
        self.assertIn("testtest", results)
        self.assertIn("домдом", results)

    #проверка обычных слов
    def test_ignores_single_words(self):
        text = "привет word один"
        results = list(create_login(text))
        self.assertEqual(results, [])

    #проверка ввода пустой строки 
    def test_empty_string(self):
        text = ""
        results = list(create_login(text))
        self.assertEqual(results, [])

    #символы из разных алфавитов 
    def test_mixed_alphabets(self):
        text = "ТестТест testtest"
        results = [m.group(0) for m in create_login(text)]
        self.assertEqual(results, ["ТестТест", "testtest"])

#чтения текста из файла
class TestFileInput(unittest.TestCase):

    def test_file_read_and_find_tandems(self):

        with open("test_text.txt", "w", encoding="utf-8") as f:
            f.write("abcabc testtest приветпривет домдом")

        with open("test_text.txt", "r", encoding="utf-8") as f:
            data = f.read()

        results = [m.group(0) for m in create_login(data)]
        self.assertIn("abcabc", results)
        self.assertIn("testtest", results)
        self.assertIn("приветпривет", results)


#Тест с консольным вводом 
class TestConsoleInput(unittest.TestCase):

    def test_console_input(self):
        text = "abcabc test hellohello word"
        results = [m.group(0) for m in create_login(text)]
        self.assertEqual(results, ["abcabc", "hellohello"])


if __name__ == "__main__":
    unittest.main()
