CREATE TABLE IF NOT EXISTS unscrapable
(
   symbol           varchar(12),
   url              varchar(255),
   site             varchar(50),
   FOREIGN KEY(symbol) REFERENCES stocks(symbol)
);