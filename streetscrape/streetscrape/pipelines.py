# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2
from psycopg2.extensions import AsIs
from dotenv import dotenv_values, find_dotenv

class StreetscrapePipeline:
    def __init__(self):
        connect_params = dotenv_values(find_dotenv('db.env'))
        self.conn = psycopg2.connect(**connect_params)
        self.cur = self.conn.cursor()
        self.cur.execute("""

        -- Table: public.stocks

        -- DROP TABLE IF EXISTS public.stocks;

        CREATE TABLE IF NOT EXISTS public.stocks
        (
            symbol character varying(12) COLLATE pg_catalog."default" NOT NULL,
            name text COLLATE pg_catalog."default",
            CONSTRAINT stocks_pkey PRIMARY KEY (symbol)
        )

        TABLESPACE pg_default;

        ALTER TABLE IF EXISTS public.stocks
            OWNER to streetscrape;

        CREATE TABLE IF NOT EXISTS public.zacks
        (
            id serial,
            symbol character varying(12) COLLATE pg_catalog."default",
            grade character varying(14) COLLATE pg_catalog."default",
            price_at_rating real,
            value character varying(1) COLLATE pg_catalog."default",
            growth character varying(1) COLLATE pg_catalog."default",
            momentum character varying(1) COLLATE pg_catalog."default",
            vgm character varying(1) COLLATE pg_catalog."default",
            quant real,
            CONSTRAINT zacks_pkey PRIMARY KEY (id),
            CONSTRAINT fk_zacks FOREIGN KEY (symbol)
                REFERENCES public.stocks (symbol) MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION
        )

        TABLESPACE pg_default;

        ALTER TABLE IF EXISTS public.zacks
            OWNER to streetscrape;

            -- Table: public.thestreet

        -- DROP TABLE IF EXISTS public.thestreet;

        CREATE TABLE IF NOT EXISTS public.thestreet
        (
            id serial,
            symbol character varying(12) COLLATE pg_catalog."default",
            grade character varying(14) COLLATE pg_catalog."default",
            price_at_rating real,
            quant real,
            CONSTRAINT thestreet_pkey PRIMARY KEY (id),
            CONSTRAINT fk_thestreet FOREIGN KEY (symbol)
                REFERENCES public.stocks (symbol) MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION
        )

        TABLESPACE pg_default;

        ALTER TABLE IF EXISTS public.thestreet
            OWNER to streetscrape;

        CREATE TABLE IF NOT EXISTS ratings_changes
        (
        id              serial PRIMARY KEY,
        date_updated    timestamp     DEFAULT CURRENT_TIMESTAMP NOT NULL,
        symbol          varchar(12)   NOT NULL,
        previous_quant  float4,
        new_quant       float4,
        site            varchar(50)   NOT NULL,
        CONSTRAINT fk_ratings_changes FOREIGN KEY (symbol)
        REFERENCES stocks (symbol)
        );

        -- Column id is associated with sequence public.ratings_changes_id_seq

        ALTER TABLE IF EXISTS public.ratings_changes
        OWNER TO streetscrape;

        CREATE TABLE IF NOT EXISTS public.gurufocus
        (
        id               serial PRIMARY KEY,
        symbol           varchar(12),
        price_at_rating  float4,
        value            int,
        growth           int,
        momentum         int,
        balancesheet     int,
        profitability    int,
        quant            float4,
        CONSTRAINT fk_gurufocus FOREIGN KEY (symbol)
        REFERENCES public.stocks (symbol)
        );

        """)

        self.conn.commit()

    def get_symbols(self):
        sql = "SELECT * FROM stocks"
        self.cur.execute(sql)
        results =  self.cur.fetchall()
        self.cur.close()
        self.conn.close()
        return results

    def generic_insert(self,table_name,item):
        insert_sql = "INSERT INTO " + table_name + "(%s) VALUES %s"
        columns = [key for key in item.keys()]
        values = [item[column] for column in columns]
        self.cur.execute(insert_sql, (AsIs(','.join(columns)),tuple(values)))
        self.conn.commit()

    def insert_change(self, symbol, prev, new, site):
        insert_sql = """
            INSERT INTO ratings_changes (symbol, previous_quant, new_quant, site)
            VALUES (%s,%s,%s,%s)
        """
        self.cur.execute(insert_sql,(symbol,prev,new,site))


    def process_thestreet_item(self, item):
        sql = "SELECT quant FROM thestreet WHERE symbol = %s"
        self.cur.execute(sql,(item['symbol'],))
        quant = None
        result = self.cur.fetchone()
        if result is not None:
            [quant] = result
        if quant is None and item['quant'] is not None:
            print("INSERT TO THE STREET")
            self.generic_insert('thestreet',item)
        else:
            if float(quant) != float(item['quant']):
                print("UPDATE THESTREET for symbol %s" % item['symbol'])

                update_sql = """
                UPDATE thestreet
                SET grade=%s, price_at_rating=%s, quant=%s
                WHERE symbol = %s
                """
                values = (item['grade'],item['price_at_rating'],item['quant'], item['symbol'])
                self.cur.execute(update_sql,values)
                self.insert_change(item['symbol'],quant,item['quant'],'thestreet')
                self.conn.commit()

        self.conn.commit()

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

        self.conn.commit()

        return item

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
            if float(quant) != float(item['quant']):
                update_sql = """
                UPDATE gurufocus
                SET momentum=%s, price_at_rating=%s, value=%s, growth=%s, momentum=%s,profitability=%s,balancesheet=%s,quant=%s
                WHERE symbol = %s
                """
                values = (item['momentum'],item['price_at_rating'],item['value'], item['growth'], item['momentum'], item['profitability'],item['balancesheet'],item['quant'], item['symbol'])
                self.cur.execute(update_sql,values)
                self.insert_change(item['symbol'],quant,item['quant'],'gurufocus')
                self.conn.commit()

        self.conn.commit()

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

    def process_item(self,item,spider):
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
        self.cur.close()
        self.conn.close()







