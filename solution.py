import feedparser
from dateutil.parser import parse as dt_parser


class StoreData:
    def __init__(self):
        self.output = []

    def write_data(self, entries):
        self.output = []

        for item in entries:
            title = item['title']
            link = item['link']
            desc = item['summary_detail']['value']
            published = dt_parser(item['published']).strftime("%m.%d.%Y %H:%M")
            if len(item['links']) == 2:
                links = item['links'][1]
            else:
                links = item['links'][0]
            image = None

            try:
                content_type = links.get('type', None)
                if content_type == 'image/jpeg':
                    image = links['href']
            except IndexError:
                pass

            self.output.append(
                {
                    'title': title,
                    'link': link,
                    'desc': desc,
                    'published': published,
                    'image': image
                }
            )


class Grabber:
    def __init__(self):
        self.lenta = Lenta()
        self.interfax = Interfax()
        self.kommersant = Kommersant()
        self.m24 = M24()


class Lenta(StoreData):
    def __init__(self):
        self.rss_url = 'http://lenta.ru/rss'
        super().__init__()

    def news(self, limit: int = None):
        response = feedparser.parse(self.rss_url)
        if response.get('status') != 301:
            return
        entries = response['entries']
        self.__write_data(entries)

        if limit is not None:
            return self.output[:limit]

        return self.output

    def __write_data(self, entries):
        return super().write_data(entries)


class Interfax(StoreData):
    def __init__(self):
        self.rss_url = 'http://www.interfax.ru/rss.asp'
        super().__init__()

    def news(self, limit: int = None):
        response = feedparser.parse(self.rss_url)
        if response.get('status') != 301:
            return
        entries = response['entries']

        self.__write_data(entries)

        if limit is not None:
            return self.output[:limit]

        return self.output

    def __write_data(self, entries):
        return super().write_data(entries)


class Kommersant(StoreData):
    def __init__(self):
        self.rss_url = 'http://www.kommersant.ru/RSS/news.xml'
        super().__init__()

    def news(self, limit: int = None):
        response = feedparser.parse(self.rss_url)
        if response.get('status') != 301:
            return
        entries = response['entries']

        self.__write_data(entries)

        if limit is not None:
            return self.output[:limit]

        return self.output

    def __write_data(self, entries):
        return super().write_data(entries)


class M24(StoreData):
    def __init__(self):
        self.rss_url = 'http://www.m24.ru/rss.xml'
        super().__init__()

    def news(self, limit: int = None):
        response = feedparser.parse(self.rss_url)
        if response.get('status') != 301:
            return
        entries = response['entries']

        self.__write_data(entries)

        if limit is not None:
            return self.output[:limit]

        return self.output

    def __write_data(self, entries):
        return super().write_data(entries)
