import requests
import dateparser
from bs4 import BeautifulSoup

from news_parser.settings import config
from parser_app.models import News, Category

class RSSOverlord():

    """RSSOverlord class defines infrastructure to retrieve RSS data and store it to database

    Usage:
    rssoverl = RSSOverlord()

    External methods:
    rssoverl.update_feed(): updates rss feed, obtaining only fresh entries since the last update and stores them to DB


    """

    class RssOverlordException(Exception):
        pass

    def __init__(self):
        try:
            self.lenta_url = config['rss_url']
        except KeyError:
            raise self.RssOverlordException('No rss_url found in config file')

    def _query_rss(self):
        try:
            response = requests.get(self.lenta_url)
        except Exception as e:
            raise self.RssOverlordException('Can\'t retrieve rss data. Error:', e.args)

        return response

    def _news_retriever(self):
        raw_data = self._query_rss().text

        souped_data = BeautifulSoup(raw_data, 'html.parser')

        return souped_data.find_all('item')

    def _save_to_db(self, date):
        news_retriever = self._news_retriever()
        bunch_of_news = []
        if not date:
            bunch_of_news = news_retriever
        else:
            for index, i in enumerate(news_retriever):
                if dateparser.parse(i.pubdate.text, settings={'TIMEZONE': 'Europe/Moscow'}) > date:
                    bunch_of_news.append(i)
                else:
                    break

        for item in bunch_of_news:
            print(item.title.text)
            try:
                item_category = Category.objects.filter(category_name=item.category.text)[0]

                news_db_obj = News(title=item.title.text, description=item.description.text,
                               time=dateparser.parse(item.pubdate.text, settings={'TIMEZONE': 'Europe/Moscow'}),
                               category=item_category)
            except IndexError:

                new_category = Category(category_name=item.category.text)
                new_category.save()
                news_db_obj = News(title=item.title.text, description=item.description.text,
                                   time=dateparser.parse(item.pubdate.text, settings={'TIMEZONE': 'Europe/Moscow'}),
                                   category=new_category)
            news_db_obj.save()

    def update_feed(self):
        if News.objects.values('time').order_by('-time'):
            latest_date = News.objects.values('time').order_by('-time')[0]['time']
        else:
            latest_date = None

        self._save_to_db(latest_date)













