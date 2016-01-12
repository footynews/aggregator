from base import Aggregator

class TheGuardian(Aggregator):

	url = 'http://www.theguardian.com/football'

	def __init__(self):
		super().__init__()

	def extract(self, soup):
		pass


if __name__ == '__main__':
	the_guardian = TheGuardian()
	soup = TheGuardian.make_soup(the_guardian.url)