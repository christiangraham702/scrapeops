import scrapy
from scrapy_playwright.page import PageMethod
from server_scraper.items import OfferUpItem
from scrapy.selector import Selector
from itertools import zip_longest


class OfferupSpider(scrapy.Spider):
    name = 'offerup'
    allowed_domains = ['offerup.com']
    start_urls = ['http://offerup.com/']

    custom_settings = {
        'DOWNLOAD_HANDLERS': "{'http': 'scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler', 'https': 'scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler'}",
        'TWISTED_REACTOR': 'twisted.internet.asyncioreactor.AsyncioSelectorReactor',
        'PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT': '100000',
        'PLAYWRIGHT_LAUNCH_OPTIONS': '{"headless": True}',
    }

    def start_requests(self):
        yield scrapy.Request(
            url="https://offerup.com/search?q=baby+formula",
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_context": "new",
                "playwright_page_methods": [
                    PageMethod("wait_for_selector",
                               'div > a:nth-child(20)'),
                ],
            },
            errback=self.errback,
        )

    async def parse(self, response):
        products_selectors_xpath = response.xpath('//a/@aria-label').getall()
        page = response.meta["playwright_page"]
        for i in range(2, 40):
            count = i * 10
            await page.evaluate('window.scrollBy(0, document.body.scrollHeight)')
            await page.wait_for_selector(f'div > a:nth-child({count})')
        html = await page.content()
        await page.close()
        item_info = Selector(text=html).xpath('//a/@aria-label').getall()
        link = Selector(text=html).xpath('//a/@href').getall()
        # f_products_selectors_xpath = response.xpath(
        #     '//a/@aria-label').getall()
        data = list(zip_longest(item_info, link))
        for sel in data:
            test_item = PwHopeItem()
            test_item['data_string'] = sel
            test_item['link'] = 'https://offerup.com' + sel[1]
            yield test_item

    async def errback(self, error):
        page = error.request.meta['playwright_page']
        await page.close()
