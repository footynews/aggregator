import datetime

from aggregator.base import Aggregator, make_soup
from aggregator.utils.calendar import month_to_code


class TheGuardian(Aggregator):

	base_url = 'http://www.theguardian.com/football'

	def extract(self):
		url = self.generate_url()
		soup = make_soup(url)
		return soup

	def generate_url(self):
		current_date = self._current_date()
		url = '{0}/{1}/{2}/{3}/all'.format(TheGuardian.base_url, *current_date)
		return url

	def _current_date(self):
		today = datetime.date.today()
		return today.year, month_to_code[today.month], today.day


if __name__ == '__main__':
	the_guardian = TheGuardian()
	print(the_guardian.extract())