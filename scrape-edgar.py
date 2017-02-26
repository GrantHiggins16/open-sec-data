"""
testing out beautifulsoup4 and basic webscraping.
the data ain't gonna mine itself.
"""

from bs4 import BeautifulSoup as BS4
import scrapy
import gzip
from lxml import etree
import os

print("hello")


def subdirs(path):
    """Yield directory names not starting with '.' under given path."""
    for entry in os.scandir(path):
        if not entry.name.startswith('.') and entry.is_dir():
            print(entry.name)
            subdir_path = path + entry.name + "/"
            for subdir in os.scandir(subdir_path):
                qtr_path = subdir_path + subdir.name + "/"
                print(subdir.name)
                for idx in os.scandir(qtr_path):
                    print(idx.name)
                


if __name__ == "__main__":
    rootdir = "/home/ubuntu/projects/open-sec-data/data/crawler.idx/"
    subdirs(rootdir)
