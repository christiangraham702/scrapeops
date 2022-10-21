
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
import logging
import json


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
            raise DropItem(f"Duplicate item found: {item!r}")
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

    def create_connection(self):
        self.conn = psycopg2.connect(
            host=hostname,
            user=username,
            dbname=database,
            password=pwd,
            port=purt
        )
        self.curr = self.conn.cursor()

    def process_item(self, item, spider):
        try:
            self.store_db(item)
        except BaseException as e:
            self.conn.rollback()
            logging.log(logging.WARNING, f"SQL ERROR: {e}")
        return item

    def store_db(self, item):
        adapter = ItemAdapter(item)
        #     insert_stat = “INSERT INTO measurement(Station, Date, Level, MeanDischarge, Discharge)
        #     VALUES (?, ?, ?, ?, ?)”, (value1, value2, value3, value4, value5)

        insert_script = '''INSERT INTO craig_data (pid, title, price, date, region, link, zip_code, dist_from_zip, num_items, state)
                           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) '''
        create_script = ''' CREATE TABLE IF NOT EXISTS craig_test2 (
                        pid             BIGINT PRIMARY KEY,
                        title           varchar(140) NOT NULL,
                        price           int,
                        date            varchar(30),
                        region          varchar(30),
                        link            varchar(150),
                        zip_code        varchar(15),
                        dist_from_zip   varchar(20),
                        num_items       varchar(10)) '''

        # checking current pid
        select_script = f"SELECT date FROM craig_data WHERE pid={adapter['pid']}"

        self.curr.execute(select_script)
        check = self.curr.fetchall()
        # if pid already in db
        if check:
            dates = check[0][0]
            # if date in db != date scraped... item has been updated
            if adapter['date'] not in dates:
                dates.append(adapter['date'])
                logging.log(
                    logging.WARNING, f"NEW DATE FOUND: updated to {adapter['date']}")
            adapter['date'] = json.dumps(dates)
        else:
            adapter['date'] = json.dumps([adapter['date']])

        insert_value = (
            adapter['pid'],
            adapter['title'],
            adapter['price'],
            adapter['date'],
            adapter['region'],
            adapter['link'],
            adapter['zip_code'],
            adapter['dist_from_zip'],
            adapter['num_items'],
            adapter['state']
        )

        self.curr.execute(insert_script, insert_value)
        self.conn.commit()
        return item

        # finally:
        #     if self.conn:
        #         # self.curr.close()
        #         # self.conn.close()
