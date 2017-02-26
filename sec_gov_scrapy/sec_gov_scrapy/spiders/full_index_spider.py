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
                item = SecGovScrapyItem()
                item['url'] = year
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
            item = SecGovScrapyItem()
            item['url'] = quarter
            print(response.url)
            # self.set_url(idx)
            yield item

    # def parse(self, response):
    #     """
    #     default scrapy parse method when no other is specified with callback
    #     """

    #     years = response.selector.xpath('//div[@id="main-content"]/table/tr/td/a/@href').extract()
    #     print(years)
        # for year in years:
        #     item = SecGovScrapyItem()
        #     item['url'] = year.xpath('/@href').extract()
        #     yield item
