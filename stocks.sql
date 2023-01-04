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