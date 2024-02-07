CREATE TABLE IF NOT EXISTS stocktwits
(
   id               serial PRIMARY KEY,
   symbol           varchar(12),
   grade            numeric,
   label            varchar(24),
   label_normalized varchar(24),
   price_at_rating  numeric,
   quant            numeric,
   FOREIGN KEY(symbol) REFERENCES stocks(symbol)
);