from dotenv import dotenv_values, find_dotenv
import psycopg2

connect_params = dotenv_values(find_dotenv('db.env'))
conn = psycopg2.connect(**connect_params)
cur = conn.cursor()

sql = """
SELECT s.symbol as Ticker, s.name as Company, t.quant as TheStreet, z.quant as Zacks, g.quant as GuruFocus,
(t.quant + z.quant + g.quant) as Total
FROM stocks s
JOIN zacks z ON z.symbol = s.symbol
JOIN gurufocus g ON g.symbol = s.symbol
JOIN thestreet t ON t.symbol = s.symbol
ORDER BY Total DESC
LIMIT 25;
"""

cur.execute(sql)
data = cur.fetchall()

with open('./best_stocks.csv','w') as ofh:
    ofh.write("Symbol,Company,TheStreet,Zacks,GuruFocus,Total\n")
    for d in data:
        ofh.write("%s,%s,%s,%s,%s,%s\n" % d)

cur.close()
conn.close()