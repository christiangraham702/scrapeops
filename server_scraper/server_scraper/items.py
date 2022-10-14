# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst


class ListCraigItem(scrapy.Item):
    title = scrapy.Field(
        output_processor=TakeFirst()
    )
    price = scrapy.Field(
        output_processor=TakeFirst()
    )
    date = scrapy.Field(
        output_processor=TakeFirst()
    )
    region = scrapy.Field(
        output_processor=TakeFirst()
    )
    link = scrapy.Field(
        output_processor=TakeFirst()
    )
    pid = scrapy.Field(
        output_processor=TakeFirst()
    )
    zip_code = scrapy.Field(
        output_processor=TakeFirst()
    )
    dist_from_zip = scrapy.Field(
        output_processor=TakeFirst()
    )
    num_items = scrapy.Field(
        output_processor=TakeFirst()
    )


class ListCraigStateItem(scrapy.Item):
    title = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst())
    date = scrapy.Field(output_processor=TakeFirst())
    region = scrapy.Field(output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
    pid = scrapy.Field(output_processor=TakeFirst())
    zip_code = scrapy.Field(output_processor=TakeFirst())
    dist_from_zip = scrapy.Field(output_processor=TakeFirst())
    num_items = scrapy.Field(output_processor=TakeFirst())
    state = scrapy.Field(output_processor=TakeFirst())
