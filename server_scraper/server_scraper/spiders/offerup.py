import scrapy


class OfferupSpider(scrapy.Spider):
    name = 'offerup'
    allowed_domains = ['offerup.com']
    start_urls = ['http://offerup.com/']

    def parse(self, response):
        pass
