from collections import defaultdict
from itertools import groupby


month_to_code = {1: 'jan', 2: 'feb', 3: 'mar', 4: 'april', 5: 'may', 6: 'jun',
                 7: 'jul', 8: 'aug', 9: 'sep', 10: 'oct', 11: 'nov', 12: 'dec'}

code_to_month = dict(zip(month_to_code.values(), month_to_code.keys()))


def generate_stats(articles):
    stats = {}
    stats['total'] = len(articles)
    valid_articles = [article for article in articles
                      if isinstance(article, Article)]
    invalid_articles = [article for article in articles
                        if isinstance(article, InvalidArticle)]
    stats['valid_articles'] = len(valid_articles)
    stats['invalid_articles'] = len(invalid_articles)
    stats['by_source'] = {}
    source_key = lambda x: x.source
    sorted_articles = sorted(articles, key=source_key)
    for key, values in groupby(sorted_articles, key=source_key):
        stats['by_source'][key] = defaultdict(int)
        for value in values:
            stats['by_source'][key][value.__class__.__name__.lower()] += 1
    return stats

def generate_report(invalid_articles, current_date):
    report_name = ('footynews_invalid_articles_daily_report_{0}'
                   .format(current_date))
    with open(report_name, 'w') as f:
        writer = csv.writer(f)
        for invalid_article in invalid_articles:
            writer.writerow(invalid_article)
    return report_name