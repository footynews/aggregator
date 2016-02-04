import datetime

from footynews.aggregator import exceptions
from footynews.aggregator.base import (Aggregator, Article, InvalidArticle,
                                       make_soup)


class ESPNFC(Aggregator):

    base_url = 'http://www.espnfc.com'
    source = 'ESPN FC'
    EXCLUDE_IF_IN_TITLE = ['LIVE:', 'WATCH:', 'LISTEN:']

    def extract(self):
        soup = make_soup(ESPNFC.base_url)
        divs = soup.find('div', {'alt': ' TOP STORIES '})
        divs = iter(divs.find_all('div', {'class': 'grid-item-content'}))
        self.articles = (self.crawl(div) for div in divs)
        return super().extract()

    def crawl(self, tag):
        url = None
        try:
            anchor = tag.find('a', {'class': 'common-link'})
            url = self.get_url(anchor)
            title = self.get_title(anchor)
            if title:
                date_published = self.get_date_published(
                                    tag.find('time')['datetime'])
                author = self.get_author(tag.find('span',
                                            {'class': 'author byline'}))
                return Article(ESPNFC.source, title, url, author,
                               date_published)
        except exceptions.WebCrawlException as e:
            return InvalidArticle(ESPNFC.source, e.__class__.__name__,
                                  e.message, url, str(e.tag))

    def get_date_published(self, tag):
        try:
            date_published = tag.split('T')[0]
            date_published = datetime.datetime.strptime(date_published,
                                                        '%Y-%m-%d').date()
            return date_published
        except (IndexError, AttributeError, ValueError, TypeError):
            raise exceptions.DatePublishedNotFoundException(e, tag)

    def get_url(self, tag):
        try:
            url = tag['href']
            url = url.replace('.us', '.com')
            return url
        except (KeyError, AttributeError, TypeError) as e:
            raise exceptions.UrlNotFoundException(e, tag)


def setup():
    return ESPNFC()


if __name__ == '__main__':
    espn_fc = ESPNFC()
    print(espn_fc.extract())
