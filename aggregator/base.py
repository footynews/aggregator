from abc import ABCMeta, abstractmethod

import requests

from bs4 import BeautifulSoup

class Aggregator(metaclass=ABCMeta):

	url = ''

	def __init__(self):
		pass

	@abstractmethod
	def extract(self, soup):
		pass

	@staticmethod
	def make_soup(url):
		response = requests.get(url)
		soup = BeautifulSoup(response.text, 'html.parser')
		return soup


