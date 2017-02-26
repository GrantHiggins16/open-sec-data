# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import requests

class SecGovScrapyPipeline(object):
    def get_path(self, item):
        """
        crawler_url's come in the form of:
        https://www.sec.gov/Archives/edgar/full-index/YYYY/QTR#/form.gz

        until the # of biz cycle changes from quarters or the name changes,
        returns the /YYYY/QTR#/form.gz portion for sane file management
        """
        return "../data/crawler.idx/" + item['crawler_url'][-21::]

    def process_item(self, item, spider):

        path = self.get_path(item)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        idx = requests.get(item['crawler_url'], stream=True)
        with open(path, "wb") as f:
            for chunk in idx.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        return item
