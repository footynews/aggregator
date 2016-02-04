import datetime

from footynews.aggregator import exceptions
from footynews.aggregator.base import (Aggregator, Article, InvalidArticle,
                                       make_soup)
from footynews.aggregator.utils import code_to_month


class FourFourTwo(Aggregator):

    base_url = 'http://www.fourfourtwo.com/features'
    source = 'FourFourTwo'
    EXCLUDE_IF_IN_TITLE = ['Video:', 'Quiz:']

    def extract(self):
        soup = make_soup(FourFourTwo.base_url)
        divs =  soup.find('div', {'class': 'content-wrapper'})
        divs = divs.find('div', {'class': 'view-content'})
        divs = iter(divs.findChildren(recursive=False))
        self.articles = (self.crawl(div) for div in divs)
        return super().extract()

    def crawl(self, tag):
        url = None
        try:
            anchor = tag.find('div', {'class': 'title'}).find('a')
            url = self.get_url(anchor)
            title = self.get_title(anchor)
            if title:
                date_published = self.get_date_published(tag.find('div',
                                                         {'class': 'created'}))
                div = make_soup(url)
                author = self.get_author(div.find('p', {'class': 'authorName'}))
                return Article(FourFourTwo.source, title, url, author,
                               date_published)
        except (exceptions.WebCrawlException, AttributeError) as e:
            return InvalidArticle(FourFourTwo.source, e.__class__.__name__,
                                  e.message, url, str(e.tag))

    def get_date_published(self, tag):
        try:
            date_published = tag.text.strip().split()
            date_published[1] = code_to_month[date_published[1][:3].lower()]
            date_published.reverse()
            date_published = datetime.datetime(*map(int, date_published)).date()
            return date_published
        except (IndexError, AttributeError, ValueError):
            raise exceptions.DatePublishedNotFoundException(e, tag)

    def get_url(self, tag):
        try:
            url = tag['href']
            url = url.split('/')[-1]
            url = FourFourTwo.base_url + '/' + url
            return url
        except (KeyError, IndexError, AttributeError, ValueError, TypeError):
            raise exceptions.UrlNotFoundException(e, tag)


def setup():
    return FourFourTwo()


if __name__ == '__main__':
    fourfourtwo = FourFourTwo()
    print(fourfourtwo.extract())