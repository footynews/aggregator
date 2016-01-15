import collections
from abc import ABCMeta, abstractmethod

import requests
from bs4 import BeautifulSoup


Article = collections.namedtuple('Article', ['source', 'title', 'url', 'author',
                                             'date_published'])

InvalidArticle = collections.namedtuple('InvalidArticle', ['source', 'exception'])


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
    def crawl(self, tag):
        pass

    @abstractmethod
    def get_author(self, tag):
        pass

    @abstractmethod
    def get_date_published(self, tag):
        pass

    @abstractmethod
    def get_title(self, tag):
        pass

    @abstractmethod
    def get_url(self, tag):
        pass

    
