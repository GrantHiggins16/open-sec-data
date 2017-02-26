"""
testing out beautifulsoup4 and basic webscraping.
the data ain't gonna mine itself.
"""

from bs4 import BeautifulSoup as BS4
import scrapy
import gzip
from lxml import etree
import os

rootdir = "~/projects/open-sec-data/data/crawler.idx"

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        print(os.path.join(subdir, file))
