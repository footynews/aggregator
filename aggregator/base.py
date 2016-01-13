from abc import ABCMeta, abstractmethod

import requests

from bs4 import BeautifulSoup


def make_soup(url):
		response = requests.get(url)
		soup = BeautifulSoup(response.text, 'html.parser')
		return soup


class Aggregator(metaclass=ABCMeta):

	base_url = ''

	@abstractmethod
	def extract(self):
		pass

	@abstractmethod
	def generate_url(self):
		pass


