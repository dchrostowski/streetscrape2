CREATE TABLE IF NOT EXISTS gurufocus
(
   id               serial PRIMARY KEY,
   symbol           varchar(12),
   price_at_rating  numeric,
   value            integer,
   growth           integer,
   momentum         integer,
   balancesheet     integer,
   profitability    integer,
   quant            numeric,
   FOREIGN KEY(symbol) REFERENCES stocks(symbol)
);