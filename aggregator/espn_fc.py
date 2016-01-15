import datetime

from aggregator import exceptions
from aggregator.base import Aggregator, Article, InvalidArticle, make_soup

EXCLUDE_IF_IN_TITLE = ['LIVE:', 'WATCH:', 'LISTEN:']

class ESPNFC(Aggregator):

    base_url = 'http://www.espnfc.com/?country-view=www&lang-view=en'
    source = 'ESPN FC'

    def extract(self):
        soup = make_soup(ESPNFC.base_url)
        divs = soup.find('div', {'alt': ' TOP STORIES '})
        divs = iter(divs.find_all('div', {'class': 'grid-item-content'}))
        articles = (self.crawl(div) for div in divs)
        return list(article for article in articles if article is not None)

    def crawl(self, tag):
        try:
            anchor = tag.find('a', {'class': 'common-link'})
            url = self.get_url(anchor)
            title = self.get_title(anchor)
            if any(exclude in title for exclude in EXCLUDE_IF_IN_TITLE):
                return None
            date_published = self.get_date_published(tag)
            author = self.get_author(tag)
            return Article(ESPNFC.source, title, url, author, date_published)
        except exceptions.WebCrawlException as e:
            return InvalidArticle(ESPNFC.source, e)

    def get_author(self, tag):
        try:
            author = tag.find('span', {'class': 'author byline'})
            return author.text.strip()
        except AttributeError as e:
            raise exceptions.AuthorNotFoundException

    def get_date_published(self, tag):
        try:
            date_published = tag.find('time')['datetime']
            date_published = date_published.split('T')[0]
            date_published = datetime.datetime.strptime(date_published,
                                                        '%Y-%m-%d').date()
            return date_published
        except (IndexError, AttributeError, ValueError, TypeError):
            raise exceptions.DatePublishedNotFoundException

    def get_title(self, tag):
        try:
            return tag.text.strip()
        except AttributeError as e:
            raise exceptions.TitleNotFoundException

    def get_url(self, tag):
        try:
            url = tag['href']
            url = url.replace('.us', '.com')
            return url
        except (KeyError, AttributeError, TypeError):
            raise exceptions.UrlNotFoundException


if __name__ == '__main__':
    espn_fc = ESPNFC()
    print(espn_fc.extract())
