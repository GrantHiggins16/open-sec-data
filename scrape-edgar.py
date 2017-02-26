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

if __name__ == "__main__":
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            print(str(os.path.join(subdir, file)))
