import os

from pluginbase import PluginBase

here = os.path.abspath(os.path.dirname(__file__))
print(here)

plugin_base = PluginBase(package='web_scraping')
plugin_source = plugin_base.make_plugin_source(searchpath=[os.path.join(here,
                                               'web_scraping_plugins')])

def main():
    for plugin in plugin_source.list_plugins():
        if plugin != 'base':
            source = plugin_source.load_plugin(plugin).setup()
            print(getattr(source, 'extract')())

if __name__ == '__main__':
    main()