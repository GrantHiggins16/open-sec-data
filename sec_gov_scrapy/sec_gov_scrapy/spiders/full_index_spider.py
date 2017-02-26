from scrapy import Spider
from scrapy.shell import inspect_response
from scrapy import Selector
from scrapy import Request
from sec_gov_scrapy.items import SecGovScrapyItem

EDGAR_ARCHIVE = "https://www.sec.gov/Archives/edgar/full-index/"


class FullIndexSpider(Spider):

    name = "full-index.sec.gov"
    working_url = ""
    # print("allowed_domains")
    # allowed_domains = ["sec.gov"]
    # start_urls = ["https://www.sec.gov/Archives/edgar/full-index/"]

    def __init__(self, *a, **kw):
        # this is probably unnecessary given my discovery of response.url
        super(FullIndexSpider, self).__init__(*a, **kw)
        self.working_url = ""

    def set_url(self, url):
        self.working_url = url
        print("working_url: {}".format(self.working_url))

    def start_requests(self):
        print("start_urls")
        yield Request(url=EDGAR_ARCHIVE,
                      callback=self.parse_years)

    def parse_years(self, response):
        """
        years parser to extract initial urls from year entries in main index
        """
        print("parse_years")
        years = response.selector.xpath(
            '//div[@id="main-content"]/table/tr/td/a/@href').extract()

        for year in years:
            if year[:-1:].isnumeric():
                print(year)
                # item = SecGovScrapyItem()
                # item['year_dir'] = year
                quarters = EDGAR_ARCHIVE+year
                # self.set_url(quarters)
                print(response.url)
                yield Request(quarters, callback=self.parse_quarters)
                # yield item
            # item = SecGovScrapyItem()
            # item['url'] = year.xpath('@href').extract()
            # yield item

    def parse_quarters(self, response):
        """
        parser to extract quarters urls using a given years urls from
        parse_years
        """
        quarters = response.selector.xpath(
            '//*[@id="main-content"]/table/tr/td/a/@href').extract()

        for quarter in quarters:
            print(quarter)
            # item = SecGovScrapyItem()
            # item['qtr_dir'] = quarter
            print(response.url)
            crawler_idx = response.url + quarter + "form.gz"
            # item['idx_url'] = idx
            # yield item
            yield Request(url=crawler_idx, callback=self.parse_crawler)
            # yield item

    def parse_crawler(self, response):
        """
        default scrapy parse method when no other is specified with callback
        """
        print(response.url)
        print(response.body)
        item = SecGovScrapyItem()
        item['crawler_url'] = response.url
        item['crawler_body'] = response.body
        # yield item


        # idx_files = response.selector.xpath(
        #     '//*[@id="main-content"]/table/tr/td/a/@href').extract()
