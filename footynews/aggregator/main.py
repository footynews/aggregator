import datetime
import os

from pluginbase import PluginBase

from footynews.aggregator.tasks.send_email import send_email

here = os.path.abspath(os.path.dirname(__file__))

plugin_base = PluginBase(package='web_scraping')
plugin_source = plugin_base.make_plugin_source(searchpath=[os.path.join(here,
                                               'web_scraping_plugins')])

from_addr = os.env['FOOTYNEWS_ADMIN_EMAIL']
password = os.env['FOOTYNEWS_ADMIN_PASSWORD']
subject = 'FootyNews Web Scraping Report - {0}'.format(datetime.date.today())

def main():
    for plugin in plugin_source.list_plugins():
            source = plugin_source.load_plugin(plugin).setup()
            print(getattr(source, 'extract')())


if __name__ == '__main__':
    main()