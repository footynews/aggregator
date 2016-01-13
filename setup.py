from setuptools import setup, find_packages

__title__ = 'footynews-aggregator'
__author__ = 'Usman Ehtesham Gul'
__email__ = 'uehtesham90@gmail.com'
__license__ = 'Apache v2.0'
__version__ = '0.0.1'
__url__ = 'https://github.com/footynews/aggregator.git'

with open('requirements.txt') as f:
    requires = f.read().splitlines()

with open("LICENSE") as f:
    license = f.read()

classifiers = [
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stablegit
    'Development Status :: 3 - Alpha',

    # Indicate who your project is intended for
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',

    # Pick your license as you wish (should match "license" above)
    'License :: OSI Approved :: MIT License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 3.4',
]

setup(
    name=__title__,
    version=__version__,
    description='Aggregate football articles from various sources',
    author=__author__,
    license=license,
    classifiers=classifiers,
    keywords="python football soccer articles",
    author_email=__email__,
    url=__url__,
    packages=find_packages(exclude='tests'),
    install_requires=requires,
)
