-- Table: public.thestreet

-- DROP TABLE IF EXISTS public.thestreet;

CREATE TABLE IF NOT EXISTS public.thestreet
(
    id integer serial,
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