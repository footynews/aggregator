import collections
from abc import ABCMeta, abstractmethod

import requests
from bs4 import BeautifulSoup


Article = collections.namedtuple('Article', ['source', 'title', 'url', 'author',
                                             'date_published'])


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
    def crawl(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_author(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_date_published(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_title(self, *args, **kwargs):
        pass

    
