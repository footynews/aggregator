import datetime

from urllib.parse import urlparse

from aggregator import exceptions
from aggregator.base import Aggregator, Article, InvalidArticle, make_soup
from aggregator.utils.calendar import code_to_month

class FourFourTwo(Aggregator):

    base_url = 'http://www.fourfourtwo.com/features'
    source = 'FourFourTwo'

    def extract(self):
        soup = make_soup(FourFourTwo.base_url)
        divs =  soup.find('div', {'class': 'content-wrapper'})
        divs = divs.find('div', {'class': 'view-content'})
        divs = iter(divs.findChildren(recursive=False))
        articles = (self.crawl(div) for div in divs)
        return list(articles)

    def crawl(self, soup):
        try:
            title, url = self.get_title_and_url(soup)
            date_published = self.get_date_published(soup)
            author = self.get_author(make_soup(url))
            return Article(FourFourTwo.source, title, url, author, date_published)
        except exceptions.WebCrawlException as e:
            return InvalidArticle(FourFourTwo.source, url, e)

    def get_author(self, soup):
        author = soup.find('p', {'class': 'authorName'})
        if author and author.text:
            return author.text.strip()
        raise exceptions.AuthorNotFoundException

    def get_date_published(self, soup):
        date_published = soup.find('div', {'class': 'created'})
        if date_published and date_published.text:
            date_published = date_published.text.strip().split()
            date_published[1] = code_to_month[date_published[1][:3].lower()]
            date_published.reverse()
            date_published = datetime.datetime(*map(int, date_published)).date()
            return date_published
        raise exceptions.DatePublishedNotFoundException

    def get_title_and_url(self, soup):
        a_href = soup.find('div', {'class': 'title'}).find('a')
        if a_href and a_href.text:
            title = a_href.text
            url = a_href['href']
            url = url.split('/')[-1]
            url = FourFourTwo.base_url + '/' + url
            return title, url
        raise exceptions.TitleNotFoundException

if __name__ == '__main__':
    fourfourtwo = FourFourTwo()
    print(fourfourtwo.extract())