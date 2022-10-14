
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import psycopg2


class ServerScraperPipeline:
    def process_item(self, item, spider):
        return item


class ListToDataPipeline:

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        adapter['date'] = adapter['date'][0]
        adapter['link'] = adapter['link'][0]
        adapter['num_items'] = adapter['num_items'][0]
        adapter['region'] = adapter['region'][0]
        # adapter['state'] = adapter['state'][0]
        adapter['title'] = adapter['title'][0]
        return item


class PriceToFloatPipeLine:

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter.get('price'):
            floatPrice = float(adapter['price'][0])
            adapter['price'] = floatPrice
            return item
        else:
            adapter['price'] = 0.0
            return item


class DupePipeline:
    def __init__(self):
        self.names_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter['pid'][0] in self.names_seen:
            raise DropItem('Duplicate item found at ')
        else:
            self.names_seen.add(adapter['pid'][0])
            return item


class SaveToPostgresPipeline(object):
    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.connection = psycopg2.connect(
            host='db-postgresql-scrapy123-do-user-12631638-0.b.db.ondigitalocean.com',
            user='doadmin',
            database='craigslist_loot',
            password='AVNS_i9jF4-8wV7KUn9TFYE_',
            port='25060',
            sslmode='require'
        )
        self.curr = self.connection.cursor()

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        try:
            self.curr.execute(""" INSERT INTO loot_test (pid, title, price, date, region, link, zip_code, dist_from_zip, num_items) values (%f, %s, %f, %s, %s, %s, %s, %s)""", (
                item['pid'],
                item['title'],
                item['price'],
                item['date'],
                item['region'],
                item['link'],
                item['zip_code'],
                item['dist_from_zip'],
                item['num_items']
            ))
        except BaseException as e:
            print(e)
        self.connection.commit()
