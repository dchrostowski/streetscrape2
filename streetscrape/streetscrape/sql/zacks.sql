CREATE TABLE IF NOT EXISTS zacks
(
   id               serial PRIMARY KEY,
   symbol           varchar(12),
   grade            varchar(14),
   price_at_rating  numeric,
   value            varchar(1),
   growth           varchar(1),
   momentum         varchar(1),
   vgm              varchar(1),
   quant            numeric,
   FOREIGN KEY(symbol) REFERENCES stocks(symbol)
);