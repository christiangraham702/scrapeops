
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


class PriceToFloatPipeLine:

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter.get('price'):
            floatPrice = int(adapter['price'])
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

        if adapter['pid'] in self.names_seen:
            raise DropItem('Duplicate item found at ')
        else:
            self.names_seen.add(adapter['pid'])
            return item


class SaveToPostgresPipeline(object):
    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.conn = psycopg2.connect(
            host='db-postgresql-scrapy123-do-user-12631638-0.b.db.ondigitalocean.com',
            user='doadmin',
            dbname='craigslist_loot',
            password='AVNS_i9jF4-8wV7KUn9TFYE_',
            port='25060'
        )
        self.curr = self.conn.cursor()

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        try:
            insert_script = '''INSERT INTO craigs_loot(pid, title, price, date, region, link, zip_code, dist_from_zip, num_items)
                               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) 
            '''
            create_script = ''' CREATE TABLE IF NOT EXISTS craigs_loot (
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
                item['pid'],
                item['title'],
                item['price'],
                item['date'],
                item['region'],
                item['link'],
                item['zip_code'],
                item['dist_from_zip'],
                item['num_items']
            )

            self.curr.execute(create_script)
            self.curr.execute(insert_script, insert_value)
            self.conn.commit()

        except Exception as e:
            print(e)
        finally:
            self.curr.close()
            self.conn.close()
