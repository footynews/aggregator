import csv
import os
from collections import defaultdict

from footynews.aggregator.base import Article, InvalidArticle
from footynews.send_email import send_email

body_template_text = 'daily_report_text.j2'

body_template_html = 'daily_report_html.j2'

class DailyReport:

    def __init__(self, current_date):
        self.current_date = current_date
        self.stats = defaultdict(int)
        self.invalid_articles = []

    def update_stats(self, article):
        self.stats['total'] += 1
        if isinstance(article, Article):
            self.stats['valid_articles'] += 1
            self.stats['valid_{0}'.format(
                article.source.lower().replace(' ', '_'))] += 1
        elif isinstance(article, InvalidArticle):
            self.stats['invalid_articles'] += 1
            self.stats['invalid_{0}'.format(
                article.source.lower().replace(' ', '_'))] += 1

    def update_report(self, article):
        self.invalid_articles.append(article)

    def generate_report(self):
        report_name = ('footynews_invalid_articles_daily_report_{0}.csv'
                       .format(self.current_date))
        report_path = os.path.join('/tmp', report_name)
        with open(report_path, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['Source', 'Exception', 'Message', 'Tag'])
            writer.writerows(self.invalid_articles)
        return report_path

    def reset(self):
        self.stats = {}
        self.invalid_articles = []

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