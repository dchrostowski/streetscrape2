# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2
from dotenv import dotenv_values, find_dotenv


class SecurityPipeline:

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

        """)

        self.conn.commit()


    def process_item(self, item, spider):
        sql = """
            INSERT INTO stocks (symbol,name)
            VALUES (%s,%s)
            ON CONFLICT (symbol) DO UPDATE
            SET symbol = excluded.symbol
                name = excluded.name;
            """

        self.cur.execute(sql,(item['symbol'],item['name']))
        self.conn.commit()

        return item

    def close_spider(self,spider):
        self.cur.close()
        self.conn.close()