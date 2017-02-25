"""
testing out beautifulsoup4 and basic webscraping.
the data ain't gonna mine itself.
"""

from bs4 import BeautifulSoup as BS4
import scrapy
import gzip
from lxml import etree

EDGAR_ARCHIVE = "https://www.sec.gov/Archives/edgar/full-index/"
QTR = "QTR"


 document = open("", "r")
soup = BS4(document, 'html.parser')
print(soup.get_text())   
