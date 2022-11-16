import scrapy
from server_scraper.items import ListCraigStateItem
from server_scraper.stuff import state_links, get_base_url
import datetime
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose
from server_scraper.funcs import get_base_url, get_num_listings, get_state, is_listings

# MAIN SPIDER, RUNS THROUGH ALL STATES


class StateScraperSpider(scrapy.Spider):
    name = 'state_scraper'
    allowed_domains = ['craigslist.org']
    start_urls = ['http://craigslist.org/']
    today = datetime.datetime.now()

    # go to each craigslist page
    def parse(self, response):
        self.query = f'/search/sss?query={self.search}'
        self.logger.info('Parse function called on %s', response.url)
        for state in state_links:
            for link in state_links[state]:
                yield scrapy.Request(link+self.query, callback=self.parse_listings)

    # parse each page for listings

    def parse_listings(self, response):
        # checks for listings
        if is_listings(response):
            # pages to parse
            page_count = response.xpath(
                '//span[@class="rangeTo"]/text()').get()
            page_count = int(page_count)
            counter = 0
            # iterating through each pid and getting info for each one
            for pid in response.xpath('//li[@class="result-row"]/@data-pid').getall():
                l = ItemLoader(item=ListCraigStateItem(), response=response)
                # finds the number of items
                l.add_xpath(
                    'num_items', '//span[@class="totalcount"]/text()', MapCompose(get_num_listings))
                l.add_xpath(
                    'num_items', '//span[@class="button pagenum"]/text()', MapCompose(get_num_listings))
                num_items = l.get_output_value('num_items')
                num_items = int(num_items[0])
                l.add_xpath(
                    'zip_code', '//div[@class="searchgroup"]/input[@name="postal"]/@value')
                l.add_value('pid', float(pid))
                l.add_value('link', response.url)
                l.add_xpath(
                    'title', f'//li[@data-pid="{pid}"]//h3[@class="result-heading"]/a/text()')
                l.add_xpath(
                    'date', f'//li[@data-pid="{pid}"]//time/@datetime')
                l.add_xpath(
                    'region', f'//li[@data-pid="{pid}"]//span[@class="nearby"]/@title')
                l.add_xpath(
                    'dist_from_zip', f'//li[@data-pid="{pid}"]//span[@class="maptag"]/text()')
                l.add_xpath(
                    'price', f'//li[@data-pid="{pid}"]//span[@class="result-price"]/text()')
                l.add_value('state', get_state(
                    response.url, len(self.query)))
                counter += 1
                yield l.load_item()
            # checking if need to go to next page
            if num_items > 120:
                next_page = response.xpath(
                    '//span[@class="buttons"]/a[@class="button next"]//@href').get()
                base_url = get_base_url(response.url)
                yield scrapy.Request(base_url+next_page, callback=self.parse_page)
