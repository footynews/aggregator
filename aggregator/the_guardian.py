import datetime

from urllib.parse import urlparse

from aggregator.base import Aggregator, Article, InvalidArticle, make_soup
from aggregator import exceptions
from aggregator.utils.calendar import month_to_code, code_to_month


class TheGuardian(Aggregator):

    base_url = 'http://www.theguardian.com/football'
    source = 'The Guardian'

    def extract(self):
        url = self._generate_url()
        soup = make_soup(url)
        divs =  iter(soup.find_all('div', {'class': 'fc-item__container'}))
        articles = (self.crawl(div) for div in divs)
        return list(article for article in articles if article is not None)

    def crawl(self, tag):
        try:
            anchor = tag.find('a')
            url = self.get_url(anchor)
            if not url:
                return None
            title = self.get_title(anchor)
            div = make_soup(url)
            div = div.find('div', {'class': 'content__meta-container'})
            author = self.get_author(div)
            date_published = self.get_date_published(div)
            return Article(TheGuardian.source, title, url, author, date_published)
        except exceptions.WebCrawlException as e:
            return InvalidArticle(TheGuardian.source, e)

    def get_author(self, tag):
        try:
            author = tag.find('a', {'rel': 'author'})
            return author.text.strip()
        except AttributeError as e:
            raise exceptions.AuthorNotFoundException

    def get_date_published(self, soup):
        try:
            date_published = soup.find('p', {'class': 'content__dateline'})
            date_published = date_published.findChildren()[0].text
            _, *date_published, _, _ = date_published.split()
            date_published[1] = code_to_month[date_published[1][:3].lower()]
            date_published.reverse()
            date_published = datetime.datetime(*map(int, date_published)).date()
            return date_published
        except (IndexError, AttributeError, ValueError):
            raise exceptions.DatePublishedNotFoundException

    def get_title(self, tag):
        try:
            return tag.text.strip()
        except AttributeError as e:
            raise exceptions.TitleNotFoundException

    def get_url(self, tag):
        try:
            url = tag['href']
            return url if self._is_valid_article(url) else None
        except (KeyError, TypeError):
            raise exceptions.UrlNotFoundException


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


if __name__ == '__main__':
    the_guardian = TheGuardian()
    print(the_guardian.extract())
