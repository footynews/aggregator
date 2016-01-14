import datetime

from urllib.parse import urlparse

from aggregator.base import Aggregator, make_soup
from aggregator.utils.calendar import month_to_code, code_to_month


class TheGuardian(Aggregator):

	base_url = 'http://www.theguardian.com/football'
	name = 'The Guardian'

	def extract(self):
		url = self.generate_url()
		soup = make_soup(url)
		divs =  iter(soup.find_all('div', {'class': 'fc-item__content'}))
		valid_hrefs = (href for href in self._extract_valid_href(divs))
		articles = (self.crawl(href) for href in valid_hrefs)
		return list(articles)

	def _extract_valid_href(self, divs):
		for div in divs:
			href = div.find('a')['href']
			if self._is_blog(href):
				yield href

	def crawl(self, url):
		soup = make_soup(url)
		title = self.get_title(soup, 'h1', {'class': 'content__headline'})
		div = soup.find('div', {'class': 'content__meta-container'})
		author = self.get_author(div, 'a', {'rel': 'author'})
		date_published = self.get_date_published(div, 'p',
												 {'class': 'content__dateline'})
		return TheGuardian.source , title, url, author, date_published

	def get_author(self, soup, *tag):
		author = soup.find('a', {'rel': 'author'})
		author = soup.find(*tag)
		if author:
			return author.text

	def get_date_published(self, soup, *tag):
		date_published = soup.find('p', {'class': 'content__dateline'})
		date_published = soup.find(*tag)
		date_published = date_published.findChildren()[0].text
		_, *date_published, _, _ = date_published.split()
		date_published[1] = code_to_month[date_published[1][:3].lower()]
		date_published.reverse()
		date_published = datetime.datetime(*map(int, date_published)).date()
		return date_published

	def get_title(self, soup, *tag):
		title = soup.find(*tag)
		if title:
			return title.text.strip()

	def generate_url(self):
		current_date = self._current_date()
		url = '{0}/{1}/{2}/{3}/all'.format(TheGuardian.base_url, *current_date)
		return url

	def _current_date(self):
		today = datetime.date.today()
		return today.year, month_to_code[today.month], today.day

	def _is_blog(self, url):
		path = urlparse(url).path
		path = path.split('/')[:-1]
		return 'blog' in path


if __name__ == '__main__':
	the_guardian = TheGuardian()
	print(the_guardian.extract())
