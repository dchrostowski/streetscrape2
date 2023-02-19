CREATE TABLE IF NOT EXISTS ratings_changes
(
   id              serial PRIMARY KEY,
   date_updated    timestamp     DEFAULT CURRENT_TIMESTAMP NOT NULL,
   symbol          varchar(12)   NOT NULL,
   previous_quant  numeric,
   new_quant       numeric,
   site            varchar(50)   NOT NULL,
   price_at_change numeric       NULL,
   FOREIGN KEY(symbol) REFERENCES stocks(symbol)
);