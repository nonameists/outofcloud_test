import time
import unicodedata

import feedparser
import requests
from bs4 import BeautifulSoup as soup


class RssData:
    title_class = None
    div_class_article = None
    p_class = None
    img_lookup = None
    div_img_class = None
    rss_url = None

    @staticmethod
    def __write_data(entries):
        """
        Метод принимает список с объектами класса FeedParserDict.
        Забирает заголовок статьи, ссылку на статью, описание, дату публикации.
        Возвращает список словарей со статьями.
        :param entries: FeedParserDict
        :return: list of dicts
        """

        output = []

        for item in entries:
            title = item.title
            link = item.link
            desc = item.summary_detail.value
            # привод времени к отображению вида "04.04.2016 11:58"
            published = time.strftime('%m.%d.%Y %H:%M', item.published_parsed)
            image = None

            """
            Проверка на кол-во элементов по ключу links. lenta.ru и m24 возвращается список из двух элементов.
            В первом 'type': 'text/html' - используем для interfax и kommersant, они не отдают ссылку на изображение.
            Во втором 'type': 'image/jpeg' - там лежит ссылка на изображение.
            """
            if len(item.links) == 2:
                links = item.links[1]
            else:
                links = item.links[0]

            content_type = links.type
            if content_type == 'image/jpeg':
                image = links.href

            output.append(
                {
                    'title': title,
                    'link': link,
                    'desc': desc,
                    'published': published,
                    'image': image
                }
            )

        return output

    def news(self, limit: int = None):
        response = feedparser.parse(self.rss_url)
        """
        Все 4 источника при успешном запросе отдают status с кодом 301(redirect).
        Не уверен, но возможно у них изменился адрес. Пример описан тут https://www.rssboard.org/redirect-rss-feed.
        """

        if response.status != 301:
            return
        # собираем элементы и передаем в метод __write_data для формирования списка словарей с нужными нам ключами
        entries = response.entries
        news_entries = self.__write_data(entries)

        if limit is not None:
            return news_entries[:limit]

        return news_entries

    def grub(self, url):
        page_source = requests.get(url)

        if page_source.status_code == 200:
            # создаем объект класса BeautifulSoup.
            data = soup(page_source.content, 'html.parser')

            """
            Поиск заголовка. Иногда парсится текст с юнюкод символами в середине предложений, к примеру - 'xa0'
            Чтобы заменить эти символы используется unicodedata.normalize.
            
            Тут описано одно из решений этой проблемы - https://stackoverflow.com/a/48286252/11315851
            Взял второй метод с использованием unicodedata.normalize. Так как использование strip=True
            не решает проблемы.
            
            Согласно доке https://www.crummy.com/software/BeautifulSoup/bs4/doc/#get-text
            strip=True - это strip whitespace from the beginning and end of each bit of text.
            
            Абзацы статьи так же иногда парсятся с юникод символами. Для них тоже применяется unicodedata.normalize.
            """
            title = data.find('h1', self.title_class).getText(strip=True)
            title = unicodedata.normalize("NFKD", title)

            # поиск текста статьи в определенном div блоке
            raw_p = data.find('div', class_=self.div_class_article).find_all('p', {'class': self.p_class})
            # записываем список абзацев статьи
            content = [unicodedata.normalize("NFKD", item.getText(strip=True)) for item in raw_p]

            image = None

            """
            Если задан img_lookup(актуально для lenta и m24) производится поиск изображения в самой статье.
            Но изображение есть не всегда, в некоторых случаях статья иллюстрируется видеороликом.
            """
            if self.img_lookup:
                div = data.find('div', {'class': self.div_img_class})

                if div and div.img:
                    image = div.img['src']

            result = [
                {
                    'title': title,
                    'content': content,
                    'image': image
                }
            ]
            return result

        return None


class Grabber:
    def __init__(self):
        self.lenta = Lenta()
        self.interfax = Interfax()
        self.kommersant = Kommersant()
        self.m24 = M24()


class Lenta(RssData):
    rss_url = 'http://lenta.ru/rss'
    title_class = 'b-topic__title'
    div_class_article = 'b-text clearfix js-topic__text'
    img_lookup = True
    div_img_class = 'b-topic__title-image'


class Interfax(RssData):
    rss_url = 'http://www.interfax.ru/rss.asp'
    div_class_article = 'infinitblock'
    title_class = {'itemprop': 'headline'}


class Kommersant(RssData):
    rss_url = 'http://www.kommersant.ru/RSS/news.xml'
    div_class_article = 'article_text_wrapper'
    title_class = {'class': 'article_name'}
    p_class = 'b-article__text'


class M24(RssData):
    rss_url = 'http://www.m24.ru/rss.xml'
    div_class_article = 'js-mediator-article'
    img_lookup = True
    div_img_class = 'b-material-incut-m-image'
