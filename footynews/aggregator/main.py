import datetime
import os
from collections import defaultdict
from itertools import groupby

from pluginbase import PluginBase

from footynews.aggregator.base import Article, InvalidArticle
from footynews.aggregator.tasks.send_email import send_email
from footynews.aggregator.utils import generate_stats
from footynews.db.models import db_session

here = os.path.abspath(os.path.dirname(__file__))

plugin_base = PluginBase(package='web_scraping')
plugin_source = plugin_base.make_plugin_source(searchpath=[os.path.join(here,
                                               'web_scraping_plugins')])

from_addr = os.environ.get('FOOTYNEWS_ADMIN_EMAIL')
password = os.environ.get('FOOTYNEWS_ADMIN_PASSWORD')
subject = 'FootyNews Web Scraping Report {0}'


def main():
    current_date = datetime.date.today()
    articles = []
    for plugin in plugin_source.list_plugins():
            source = plugin_source.load_plugin(plugin).setup()
            articles.extend(list(getattr(source, 'extract')()))
    stats = generate_stats(articles)
    report = generate_report((article for article in articles 
                              if isinstance(article, InvalidArticle)),
                              current_date)


if __name__ == '__main__':
    main()
