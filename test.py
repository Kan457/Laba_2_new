import url_work
import unittest
from unittest.mock import patch, mock_open, MagicMock
from reg_exe import create_login
from url_work import from_my_url

# Проверяем, что функция возвращает объединённый текст из <p>-тегов
class TestFromMyUrlSuccess(unittest.TestCase):
    @patch("requests.get")
    #запрос не происходит , вместо этоговызывается фек объект
    def test_returns_combined_text(self, mock_get):
        #Создаём поддельный HTML-документ, который будто бы пришёл с сайта
        html = "<html><body><p>Да</p><p>нет</p></body></html>"
        #Создаём объект mock_response — это фейковый ответ от requests.get()
        mock_response = MagicMock()
        mock_response.content = html.encode("utf-8")
        # вернёт наш объект mock_response (а не пойдёт в интернет)
        mock_get.return_value = mock_response
        # Вызываем тестируемую функцию
        result = url_work.from_my_url("https://gist.github.com/Kan457/589b69ca0c16d69116487aeb92f2cb9d/raw")
        # Проверяем, что результат именно такой, как мы ожидаем
        self.assertEqual(result, "Нет Да")
        # Это доказывает, что наша функция действительно обращалась "к сайту"
        mock_get.assert_called_once()


# Проверяем, что функция возвращает пустую строку, если нет <p>-тегов
class TestFromMyUrlEmptyParagraphs(unittest.TestCase):
    @patch("requests.get")
    def test_returns_empty_string(self, mock_get):

        html = "<html><body><div>Нет параграфов</div></body></html>"
        mock_response = MagicMock()
        mock_response.content = html.encode("utf-8")
        mock_get.return_value = mock_response

        result = url_work.from_my_url("https://gist.github.com/Kan457/589b69ca0c16d69116487aeb92f2cb9d/raw")
        self.assertEqual(result, "")


# Проверяем обработку ошибок запросов
class TestFromMyUrlException(unittest.TestCase):
    @patch("requests.get")
    def test_handles_request_exception(self, mock_get):

        mock_get.side_effect = Exception("Ошибка соединения")

        result = url_work.from_my_url("https://gist.github.com/Kan457/589b69ca0c16d69116487aeb92f2cb9d/raw")
        self.assertIsNone(result)

# Проверяем, что из файла читаются тандемные слова
class TestFileInput(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data="abcabc testtest приветпривет домдом")
    def test_file_read_and_find_tandems(self, mock_file):
        data = open('text.txt', encoding='utf-8').read()
        results = [m.group(0) for m in create_login(data)]
        self.assertIn("abcabc", results)
        self.assertIn("testtest", results)
        self.assertIn("приветпривет", results)

# Проверяем работу create_login при консольном вводе
class TestConsoleInput(unittest.TestCase):
    @patch("builtins.input", side_effect=["abcabc test hellohello word"])
    def test_console_input(self, mock_input):
        text = input("Введите текст: ")
        results = [m.group(0) for m in create_login(text)]
        self.assertEqual(results, ["abcabc", "hellohello"])

#Проверяем извлечение текста и нахождение тандемов из HTML
class TestWebInput(unittest.TestCase):
    """Тесты режима проверки через сайт"""

    @patch("url_work.requests.get")
    def test_web_input(self, mock_get):
        html = "<html><body><p>abcabc</p><p>testtest</p><p>word</p></body></html>"
        mock_response = MagicMock()
        mock_response.content = html.encode("utf-8")
        mock_get.return_value = mock_response

        text = from_my_url("https://gist.github.com/Kan457/589b69ca0c16d69116487aeb92f2cb9d/raw")
        results = [m.group(0) for m in create_login(text)]

        self.assertIn("abcabc", results)
        self.assertIn("testtest", results)
        self.assertNotIn("word", results)


class TestTandemRepeats(unittest.TestCase):
    """Тесты для поиска тандемных повторов"""
    
    def test_finds_simple_repeats(self):
        """Находит простые повторы типа 'словослово'"""
        # Тестовая строка с тремя примерами повторов
        text = "abcabc testtest домдом"
        
        # Вызываем функцию create_login и преобразуем результаты в список строк
        results = [m.group(0) for m in create_login(text)]
        
        # Проверяем, что найдено ровно 3 повтора
        self.assertEqual(len(results), 3)
        # Проверяем, что каждый из ожидаемых повторов присутствует в результатах
        self.assertIn("abcabc", results)
        self.assertIn("testtest", results) 
        self.assertIn("домдом", results)
    
    def test_ignores_single_words(self):
        """Игнорирует одиночные слова без повторов"""
        # Строка с обычными словами без повторов
        text = "привет word один"
        
        # Вызываем функцию и преобразуем в список
        results = list(create_login(text))
        
        # Проверяем, что результат пустой (повторов не найдено)
        self.assertEqual(results, [])
    
    def test_empty_string(self):
        """Пустая строка = пустой результат"""
        # Пустая входная строка
        text = ""
        
        # Вызываем функцию с пустой строкой
        results = list(create_login(text))
        
        # Проверяем, что результат пустой
        self.assertEqual(results, [])
    
    def test_case_sensitive(self):
        """Регистр имеет значение: AbcAbc ≠ abcabc"""
        # Строка с повторами в разном регистре
        text = "AbcAbc abcabc"
        
        # Получаем результаты как список строк
        results = [m.group(0) for m in create_login(text)]
        
        # Проверяем, что найден только повтор в нижнем регистре
        # (функция чувствительна к регистру)
        self.assertEqual(results, ["abcabc"])
    
    def test_mixed_alphabets(self):
        """Работает с кириллицей и латиницей"""
        # Строка с повторами на кириллице и латинице
        text = "ТестТест testtest"
        
        # Получаем результаты как список строк
        results = [m.group(0) for m in create_login(text)]
        
        # Проверяем, что найдены оба повтора - и кириллический и латинский
        self.assertEqual(results, ["ТестТест", "testtest"])


if __name__ == "__main__":
    unittest.main()
