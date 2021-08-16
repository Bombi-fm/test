
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import re

from requests import Timeout, ConnectionError


class ArticleParser:

    def __init__(self):
        self.article_page = "https://news.google.com/search?q=russia%20when%3A30d&hl=en-US&gl=US&ceid=US%3Aen"
        self.articles_url_list = []
        self.articles_texts = []
        self.all_text = ''

    def run(self):
        self.get_article_list()
        self.get_text_from_article()
        self.word_cloud_picture()

    def get_article_list(self):
        """Получает ссылки на статьи с сайта goodle.news с ключевым словом Russia за 30 дней"""
        host = "https://news.google.com/"
        response = requests.get(self.article_page)
        if response.status_code == 200:
            root_page = BeautifulSoup(response.text, features='html.parser')
            article_list = root_page.find_all("a", {"class": "VDXfz"})

            for article in article_list:
                result = re.search(r'href="(.*);', str(article))
                article_url = result.group(0)
                article_url = re.split(r';', article_url)
                article_url = article_url[0]
                article_url = article_url.replace('href="', host)
                self.articles_url_list.append(article_url)

    def get_text_from_article(self):
        for url in self.articles_url_list:
            self.article_cleaner(url)

    def article_cleaner(self, url):
        """Получает текст статьи по url и чистит его от ненужной информации"""
        try:
            response = requests.get(url, allow_redirects=True, timeout=5)
        except (Timeout, ConnectionError) as e:
            return
        soup = BeautifulSoup(response.text, features="html.parser")

        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        self.articles_texts.append(text)

    def word_cloud_picture(self):
        for article in self.articles_texts:
            self.all_text += ' '
            self.all_text += article
        wcloud = WordCloud(max_words=50).generate(str(self.all_text))
        plt.imshow(wcloud, interpolation='bilinear')
        plt.axis('off')
        plt.show()


alpha = ArticleParser()
alpha.run()

