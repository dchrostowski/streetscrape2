CREATE TABLE IF NOT EXISTS thestreet2
(
   id               serial PRIMARY KEY,
   symbol           varchar(12),
   grade            varchar(14),
   price_at_rating  numeric,
   quant            numeric,
   FOREIGN KEY(symbol) REFERENCES stocks(symbol)
);