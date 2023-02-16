# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2
from psycopg2.extensions import AsIs
from dotenv import dotenv_values, find_dotenv
import json
from IPython import embed
from datetime import datetime, timezone
import os
SQL_FILES = ['stocks.sql','thestreet.sql','zacks.sql','gurufocus.sql', 'ratings_changes.sql','unscrapable.sql']
CWD =  os.path.dirname(os.path.abspath(__file__))
sql_file_prefix = os.path.join(CWD, 'sql/')

class StreetscrapePipeline:
    def __init__(self):

        connect_params = dotenv_values(find_dotenv('db.env'))


        self.conn = psycopg2.connect(**connect_params)
        self.cur = self.conn.cursor()
        for sql_file in SQL_FILES:
            file = "%s%s" % (sql_file_prefix,sql_file)
            with open(file,'r') as ifh:
                sql = ifh.read()
                self.cur.execute(sql)
                self.conn.commit()

        self.conn.commit()

    def get_symbols(self):
        sql = "SELECT * FROM stocks ORDER BY RANDOM ()"
        self.cur.execute(sql)
        results =  self.cur.fetchall()


        return results

    def get_unscrapable(self,site):
        sql = 'SELECT distinct(url),symbol,site FROM unscrapable WHERE site=%s'
        self.cur.execute(sql,(site,))
        results = self.cur.fetchall()


        return results

    def remove_unscrapable(self,symbol,site):
        sql = 'DELETE FROM UNSCRAPABLE WHERE symbol=%s and site=%s'
        self.cur.execute(sql,(symbol,site))
        self.conn.commit()

    def generic_insert(self,table_name,item):
        insert_sql = "INSERT INTO " + table_name + "(%s) VALUES %s"
        columns = [key for key in item.keys()]
        values = [item[column] for column in columns]
        try:
            self.cur.execute(insert_sql, (AsIs(','.join(columns)),tuple(values)))
            self.conn.commit()
            print("inserted new record for %s into %s" % (item['symbol'], table_name))
        except Exception as e:
            print(e)


    def insert_change(self, symbol, prev, new, site):
        insert_sql = """
            INSERT INTO ratings_changes (symbol, previous_quant, new_quant, site)
            VALUES (%s,%s,%s,%s)
        """
        self.cur.execute(insert_sql,(symbol,prev,new,site))
        self.conn.commit()
        print("updated record for %s on %s" % (symbol,site))


    def process_thestreet_item(self, item):
        sql = "SELECT quant FROM thestreet WHERE symbol = %s"
        self.cur.execute(sql,(item['symbol'],))
        quant = None
        result = self.cur.fetchone()
        if result is not None:
            [quant] = result
        if quant is None and item['quant'] is not None:
            self.generic_insert('thestreet',item)
        else:
            if float(quant) != float(item['quant']):
                update_sql = """
                UPDATE thestreet
                SET grade=%s, price_at_rating=%s, quant=%s
                WHERE symbol = %s
                """
                values = (item['grade'],item['price_at_rating'],item['quant'], item['symbol'])
                self.cur.execute(update_sql,values)
                self.insert_change(item['symbol'],quant,item['quant'],'thestreet')

        return item


    def process_zacks_item(self, item):
        sql = "SELECT quant FROM zacks WHERE symbol = %s"
        self.cur.execute(sql,(item['symbol'],))
        quant = None
        result = self.cur.fetchone()
        if result is not None:
            [quant] = result
        if quant is None and item['quant'] is not None:
            self.generic_insert('zacks',item)
        else:
            if float(quant) != float(item['quant']):
                update_sql = """
                UPDATE zacks
                SET grade=%s, price_at_rating=%s, value=%s, growth=%s, momentum=%s,vgm=%s,quant=%s
                WHERE symbol = %s
                """
                values = (item['grade'],item['price_at_rating'],item['value'], item['growth'], item['momentum'], item['vgm'], item['quant'], item['symbol'])
                self.cur.execute(update_sql,values)
                self.insert_change(item['symbol'],quant,item['quant'],'zacks')
                self.conn.commit()

        return item

    def should_update_gurufocus(self,symbol):
        sql = "SELECT date_updated, now() from ratings_changes WHERE site='gurufocus' and symbol = '%s' order by id desc limit 1" % symbol
        self.cur.execute(sql)
        result = self.cur.fetchone()
        if result is not None:
            (last_updated, now) = result
            diff = now - last_updated.replace(tzinfo=timezone.utc)
            minutes = diff.seconds / 60
            if(minutes < 60):
                print("TOO SOON TO UPDATE")
                return False
        return True



    def process_gurufocus_item(self,item):
        sql = "SELECT quant FROM gurufocus WHERE symbol = %s"
        self.cur.execute(sql,(item['symbol'],))
        quant = None
        result = self.cur.fetchone()
        if result is not None:
            [quant] = result
        if quant is None and item['quant'] is not None:
            self.generic_insert('gurufocus',item)
        else:
            if float(quant) != float(item['quant']) and self.should_update_gurufocus(item['symbol']):
                update_sql = """
                UPDATE gurufocus
                SET price_at_rating=%s, value=%s, growth=%s, momentum=%s,profitability=%s,balancesheet=%s,quant=%s
                WHERE symbol = %s
                """
                values = (item['price_at_rating'],item['value'], item['growth'], item['momentum'], item['profitability'],item['balancesheet'],item['quant'], item['symbol'])
                self.cur.execute(update_sql,values)
                self.insert_change(item['symbol'],quant,item['quant'],'gurufocus')

        return item

    def process_swingtradebot_item(self, item):
        sql = """
            INSERT INTO stocks (symbol,name)
            VALUES (%s,%s)
            ON CONFLICT (symbol) DO UPDATE
            SET symbol = excluded.symbol,
                name = excluded.name;
            """

        self.cur.execute(sql,(item['symbol'],item['name']))
        self.conn.commit()

        return item

    def process_unscrapable_item(self,item):
        sql = """INSERT INTO unscrapable (symbol,site,url) VALUES (%s,%s,%s)"""
        self.cur.execute(sql,(item['symbol'],item['site'], item['url']))
        self.conn.commit()



    def process_item(self,item,spider):
        print("item is:" )
        print(item)
        if item.get('url',None) is not None and item.get('site',None) is not None:
            return self.process_unscrapable_item(item)
        if spider.name == 'swingtradebot':
            return self.process_swingtradebot_item(item)
        elif spider.name == 'zacks':
            return self.process_zacks_item(item)
        elif spider.name == 'thestreet':
            return self.process_thestreet_item(item)
        elif spider.name == 'gurufocus':
            return self.process_gurufocus_item(item)
        return item

    def close_spider(self,spider):


        if spider.name == 'gurufocus':

            with open('./gurufocus_unscrapable.json', 'w') as ofh:
                unscrapable = json.dumps(spider.unscrapable)
                ofh.write(unscrapable)

        self.cur.close()
        self.conn.close()







