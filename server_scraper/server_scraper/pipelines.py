
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import psycopg2
from server_scraper.secret.info import *
from server_scraper.funcs import get_price


class ServerScraperPipeline:
    def process_item(self, item, spider):
        return item


class PriceToFloatPipeLine:

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter.get('price'):
            tmp = get_price(adapter['price'])
            floatPrice = int(tmp)
            adapter['price'] = floatPrice
            return item
        else:
            adapter['price'] = 0
            return item


class DupePipeline:
    def __init__(self):
        self.names_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter['pid'] in self.names_seen:
            raise DropItem('Duplicate item found at ')
        else:
            self.names_seen.add(adapter['pid'])
            return item


class CheckNonePipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if not adapter.get('title'):
            adapter['title'] = 'None'
        if not adapter.get('date'):
            adapter['date'] = 'None'
        if not adapter.get('region'):
            adapter['region'] = 'None'
        if not adapter.get('link'):
            adapter['link'] = 'None'
        if not adapter.get('zip_code'):
            adapter['zip_code'] = 'None'
        if not adapter.get('dist_from_zip'):
            adapter['dist_from_zip'] = 'None'
        if not adapter.get('num_items'):
            adapter['num_items'] = 'None'
        return item


class SaveToPostgresPipeline(object):
    def __init__(self):
        self.create_connection()

    def create_connection(self, spider):
        self.conn = psycopg2.connect(
            host=hostname,
            user=username,
            dbname=database,
            password=pwd,
            port=purt
        )
        self.curr = self.conn.cursor()

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        adapter = ItemAdapter(item)

        try:
            insert_script = '''insert into craigs_loot (pid, title, price, date, region, link, zip_code, dist_from_zip, num_items)
                               values (%f,%s,%i,%s,%s,%s,%s,%s,%s) 
            '''
            create_script = ''' CREATE TABLE IF NOT EXISTS craig_test2 (
                            pid             int PRIMARY KEY,
                            title           varchar(140) NOT NULL,
                            price           int,
                            date            varchar(30),
                            region          varchar(30),
                            link            varchar(150),
                            zip_code        varchar(15),
                            dist_from_zip   varchar(20),
                            num_items       varchar(10)) '''

            insert_value = (
                adapter['pid'],
                adapter['title'],
                adapter['price'],
                adapter['date'],
                adapter['region'],
                adapter['link'],
                adapter['zip_code'],
                adapter['dist_from_zip'],
                adapter['num_items']
            )

            # self.curr.execute(create_script)
            self.curr.execute(create_script)
            self.curr.execute(insert_script, insert_value)
            self.conn.commit()

        except BaseException as e:
            print(e)
        finally:
            if self.conn:
                self.curr.close()
                self.conn.close()
