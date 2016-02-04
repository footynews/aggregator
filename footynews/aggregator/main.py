import datetime
import os
from collections import defaultdict
from itertools import groupby

import sqlalchemy.exc
from pluginbase import PluginBase

from footynews.aggregator.base import Article, InvalidArticle
from footynews.daily_report import DailyReport
from footynews.db.models import Articles, db_session

here = os.path.abspath(os.path.dirname(__file__))

plugin_base = PluginBase(package='web_scraping')
plugin_source = plugin_base.make_plugin_source(searchpath=[os.path.join(here,
                                               'web_scraping_plugins')])

daily_report = DailyReport(datetime.date.today())

def main():
    articles = []
    for plugin in plugin_source.list_plugins():
            source = plugin_source.load_plugin(plugin).setup()
            for article in getattr(source, 'extract')():
                if isinstance(article, Article):
                    try:
                        db_session.add(Articles(article))
                        db_session.commit()
                    except sqlalchemy.exc.IntegrityError as  e:
                        if ('duplicate key value violates unique constraint'
                            in e.orig):
                            print("{0} already exists".format(article.url))
                            db_session.rollback()
                elif isinstance(article, InvalidArticle):
                    daily_report.update_report(article)
                daily_report.update_stats(article)
    print(daily_report.stats)
    if datetime.datetime.now().hour == 23:
        daily_report.email_report()
        daily_report.reset()


if __name__ == '__main__':
    main()
