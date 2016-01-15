import collections
from abc import ABCMeta, abstractmethod

import requests
from bs4 import BeautifulSoup


Article = collections.namedtuple('Article', ['source', 'title', 'url', 'author',
                                             'date_published'])

InvalidArticle = collections.namedtuple('InvalidArticle', ['source', 'url',
                                                           'exception'])


def make_soup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


class Aggregator(metaclass=ABCMeta):

    base_url = ''
    source = ''

    @abstractmethod
    def extract(self):
        pass

    @abstractmethod
    def generate_url(self):
        pass

    @abstractmethod
    def crawl(self, url):
        pass

    @abstractmethod
    def get_author(self, soup):
        pass

    @abstractmethod
    def get_date_published(self, soup):
        pass

    @abstractmethod
    def get_title(self, soup):
        pass

    
