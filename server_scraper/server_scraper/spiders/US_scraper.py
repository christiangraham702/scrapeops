
import scrapy
from server_scraper.items import ListCraigItem
from server_scraper.stuff import good_links, get_base_url
from scrapy.loader import ItemLoader
import datetime
from itemloaders.processors import MapCompose, TakeFirst
from server_scraper.funcs import get_base_url, get_num_listings, get_price, is_listings


class USScraperSpider(scrapy.Spider):
    name = 'US_scraper'

    allowed_domains = ['craigslist.org']
    start_urls = ['http://craigslist.org/']

    today = datetime.datetime.now()
    filename = f'craigslist_state_raid_{today.strftime("%m-%d-%Y_%H:%M")}'

#    custom_settings = {
#       'FEED_URI': f'data/{filename}.json',
#       'FEED_FORMAT': 'json'
    # 'LOG_FILE': f'data/{filename}.log'
#   }

    def parse(self, response):

        # good_links = [(link,zip)]
        for link in good_links:
            if link[1] == 'no zip code':
                continue
            search = f'/search/sss?query={self.search}&search_distance=250&postal={link[1]}'
            url = link[0]+search
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        proc = TakeFirst()
        # checks for listings
        if is_listings(response):
            # pages to parse
            page_count = response.xpath(
                '//span[@class="rangeTo"]/text()').get()
            page_count = int(page_count)
            counter = 0
            # iterating through each pid and getting info for each one
            for pid in response.xpath('//li[@class="result-row"]/@data-pid').getall():
                l = ItemLoader(item=ListCraigItem(), response=response)
                # finds the number of items
                l.add_xpath(
                    'num_items', '//span[@class="totalcount"]/text()', MapCompose(get_num_listings))
                l.add_xpath(
                    'num_items', '//span[@class="button pagenum"]/text()', MapCompose(get_num_listings))
                num_items = l.get_output_value('num_items')
                num_items = int(num_items[0])
                if counter <= num_items:
                    l.add_xpath(
                        'zip_code', '//div[@class="searchgroup"]/input[@name="postal"]/@value')
                    l.add_value('pid', int(pid))
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
                    counter += 1
                    yield l.load_item()
            # checking if need to go to next page
            if num_items > 120 and not page_count == num_items:
                next_page = response.xpath(
                    '//span[@class="buttons"]/a[@class="button next"]//@href').get()
                base_url = get_base_url(response.url)
                yield scrapy.Request(base_url+next_page, callback=self.parse_page)
