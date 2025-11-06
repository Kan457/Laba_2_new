import requests
import unittest
from bs4 import BeautifulSoup
URL_GIST = 'https://gist.github.com/Kan457/589b69ca0c16d69116487aeb92f2cb9d/raw'


def from_my_url(url_web: str):
    try:
        response = requests.get(url_web)
        data = response.content.decode("utf-8")
        soup = BeautifulSoup(data, "html.parser")
        contents = soup.findAll("p") 
        full_text = " ".join(content.get_text(strip=True) for content in contents)
        return full_text

    except requests.RequestException as e:
        print(f"Произошла ошибка: {e}")
    
    unittest.main()


if __name__ == "__main__":
    print(from_my_url(URL_GIST))