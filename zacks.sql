-- Table: public.zacks

-- DROP TABLE IF EXISTS public.zacks;

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