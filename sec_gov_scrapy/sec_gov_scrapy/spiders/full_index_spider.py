from scrapy import Spider
from scrapy.shell import inspect_response
from scrapy import Selector
from scrapy import Request
from sec_gov_scrapy.items import SecGovScrapyItem

EDGAR_ARCHIVE = "https://www.sec.gov/Archives/edgar/full-index/"

class FullIndexSpider(Spider):
    print("name")
    name = "full-index.sec.gov"
    # print("allowed_domains")
    # allowed_domains = ["sec.gov"]
    # start_urls = ["https://www.sec.gov/Archives/edgar/full-index/"]

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
            yield item
            # item = SecGovScrapyItem()
            # item['url'] = year.xpath('@href').extract()
            # yield item

    def parse_quarters(self, response):
        """
        parser to extract quarters urls using a given years urls from
        parse_years
        """
        response.selector.xpath(
            '//*[@id="main-content"]/table/tr/td/a/@href').extract()

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
