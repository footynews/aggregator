import csv
import os
import shelve
from collections import defaultdict

from footynews.aggregator.base import Article, InvalidArticle
from footynews.send_email import send_email

body_template_text = 'daily_report_text.j2'

body_template_html = 'daily_report_html.j2'

shelve_db = '/tmp/daily_report'

class DailyReport:

    def __init__(self, current_date):
        self.current_date = current_date

    def update(self, article):
        with shelve.open(shelve_db) as db:
            stats = db.get('stats', defaultdict(int))
            stats['total'] += 1
            if isinstance(article, Article):
                stats['valid_articles'] += 1
                stats['valid_{0}'.format(
                    article.source.lower().replace(' ', '_'))] += 1
            elif isinstance(article, InvalidArticle):
                stats['invalid_articles'] += 1
                stats['invalid_{0}'.format(
                    article.source.lower().replace(' ', '_'))] += 1
                invalid_articles = db.get('invalid_articles', [])
                invalid_articles.append(article)
                db['invalid_articles'] = invalid_articles
            db['stats'] = stats

    def generate_report(self):
        report_name = ('footynews_invalid_articles_daily_report_{0}.csv'
                       .format(self.current_date))
        report_path = os.path.join('/tmp', report_name)
        with open(report_path, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['Source', 'Exception', 'Message', 'URL', 'Tag'])
            writer.writerows(self.invalid_articles)
        return report_path

    def reset(self):
        with shelve.open(shelve_db, flag='n'):
            pass

    def email_report(self):
        from_addr = os.environ.get('FOOTYNEWS_ADMIN_EMAIL')
        password = os.environ.get('FOOTYNEWS_ADMIN_PASSWORD')
        to_addr = os.environ.get('FOOTYNEWS_ADMIN_EMAIL')
        subject = 'FootyNews Web Scraping Report {0}'.format(self.current_date)
        report_path = self.generate_report()
        send_email(from_addr, password, to_addr, subject, body_template_text,
                   body_template_html, self.stats, report_path)
        self.delete_report(report_path)

    def delete_report(self, report_path):
        os.remove(report_path)