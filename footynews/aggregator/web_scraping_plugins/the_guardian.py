import datetime

from urllib.parse import urlparse

from footynews.aggregator import exceptions
from footynews.aggregator.base import (Aggregator, Article, InvalidArticle,
                                       make_soup)
from footynews.aggregator.utils import month_to_code, code_to_month


class TheGuardian(Aggregator):

    base_url = 'http://www.theguardian.com/football'
    source = 'The Guardian'

    def extract(self):
        url = self._generate_url()
        soup = make_soup(url)
        divs =  iter(soup.find_all('div', {'class': 'fc-item__container'}))
        self.articles = (self.crawl(div) for div in divs)
        return super().extract()

    def crawl(self, tag):
        url = None
        try:
            anchor = tag.find('a')
            url = self.get_url(anchor)
            # Added here because URLs are filtered via method _is_valid_article
            if not url:
                return None
            title = self.get_title(anchor)
            if title:
                div = make_soup(url)
                div = div.find('div', {'class': 'content__meta-container'})
                author = self.get_author(div.find('a', {'rel': 'author'}))
                date_published = self.get_date_published(None)
                return Article(TheGuardian.source, title, url, author,
                               date_published)
        except exceptions.WebCrawlException as e:
            return InvalidArticle(TheGuardian.source, e.__class__.__name__,
                                  e.message, url, str(e.tag))

    def get_date_published(self, tag):
        # Given structure of HTML pages is w.r.t. date and since we only web
        # scrape one specific page per day, we can just return current date
        return datetime.date.today()
        # try:
        #     date_published = tag.findChildren()[0].text
        #     _, *date_published, _, _ = date_published.split()
        #     date_published[1] = code_to_month[date_published[1][:3].lower()]
        #     date_published.reverse()
        #     date_published = datetime.datetime(*map(int, date_published)).date()
        #     return date_published
        # except (IndexError, AttributeError, ValueError):
        #     raise exceptions.DatePublishedNotFoundException

    def get_url(self, tag):
        try:
            url = tag['href']
            return url if self._is_valid_article(url) else None
        except (KeyError, TypeError) as e:
            raise exceptions.UrlNotFoundException(e, tag)

    def _generate_url(self):
        current_date = self._current_date()
        url = '{0}/{1}/{2}/{3}/all'.format(TheGuardian.base_url, *current_date)
        return url

    def _current_date(self):
        today = datetime.date.today()
        return today.year, month_to_code[today.month], today.day

    def _is_valid_article(self, url):
        path = urlparse(url).path
        path = set(path.split('/')[:-1])
        return 'blog' in path or 'who-scored-blog' in path

def setup():
    return TheGuardian()


if __name__ == '__main__':
    the_guardian = TheGuardian()
    print(the_guardian.extract())
