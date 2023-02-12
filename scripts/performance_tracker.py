# https://query2.finance.yahoo.com/v8/finance/chart/ADM?period1=1651816800&period2=1697695200&interval=1d&includePrePost=true&events=div%7Csplit%7Cearn&useYfid=true&lang=en-US&region=US


from dotenv import dotenv_values, find_dotenv
import psycopg2
import requests
from datetime import datetime, timedelta
import time

connect_params = dotenv_values(find_dotenv('db.env'))
conn = psycopg2.connect(**connect_params)
cur = conn.cursor()
from IPython import embed
import json
import time

#yahoo_url = "https://query2.finance.yahoo.com/v8/finance/chart/%s?period1=%s&period2=%s&interval=1d&includePrePost=true&events=div%7Csplit%7Cearn&useYfid=true&lang=en-US&region=US" % (symbol, start_timestamp, end_timestamp)

data_cache = {}

with open('./data_cache.json') as ifh:
    data_cache = json.load(ifh)


def save_cache(data):
    with open('./data_cache.json','w') as ofh:
        json.dump(data,ofh)


def get_price_changes(min_scores,score_change_operator):

    sites = ['zacks','thestreet','gurufocus']
    new_scores = {}
    price_changes = {}

    sites = min_scores.keys()

    for site in sites:
        new_scores_sql = "SELECT DISTINCT(new_quant) FROM ratings_changes WHERE site = '%s'" % site
        cur.execute(new_scores_sql)
        data = cur.fetchall()
        new_scores[site] = [d[0] for d in data]
        price_changes[site] = []

    for site,scores in new_scores.items():
        min_score = min_scores[site]
        for score in scores:
            if score >= min_score:
                sql = "SELECT id, date_updated,symbol FROM ratings_changes where site = '%s' and new_quant = %s" % (site,score)
                cur.execute(sql)
                data = cur.fetchall()
                for d in data:
                    (id, date,symbol) = d
                    start_date = date - timedelta(days=1)
                    end_date = datetime.now() - timedelta(days=1)
                    unix_start_time = int(time.mktime(start_date.timetuple()))
                    unix_end_time = int(time.mktime(end_date.timetuple()))

                    end_sql = "SELECT date_updated,symbol FROM ratings_changes where site = '%s' and symbol = '%s' and new_quant %s %s and id > %s order by id asc limit 1" % (site,symbol,score_change_operator,score,id)
                    cur.execute(end_sql)
                    result = cur.fetchone()
                    if result is not None:
                        end_date = result[0]
                        unix_end_time = int(time.mktime(end_date.timetuple()))



                    print("%s: %s" % (date,symbol))
                    print(unix_start_time)
                    print(unix_end_time)
                    print(symbol)
                    data = data_cache.get(symbol,None)
                    if data is None:
                        time.sleep(1)
                        yahoo_url = "https://query2.finance.yahoo.com/v8/finance/chart/%s?period1=%s&period2=%s" % (symbol, unix_start_time, int(time.mktime(datetime.now().timetuple())))
                        yahoo_url += '&interval=1d&includePrePost=true&events=div%7Csplit%7Cearn&useYfid=true&lang=en-US&region=US'
                        print(yahoo_url)
                        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
                        yahoo_resp = requests.get(yahoo_url,  headers=headers)
                        if yahoo_resp.status_code == 200:
                            data = json.loads(yahoo_resp.content)
                            data_cache[symbol] = data
                            save_cache(data_cache)

                    timestamps = []
                    opens = []
                    try:
                        timestamps = data['chart']['result'][0]['timestamp']
                        opens = data['chart']['result'][0]['indicators']['quote'][0]['open']
                    except TypeError as e:
                        pass

                    price_data = {}
                    for i in range(len(timestamps)):
                        price_data[timestamps[i]] = opens[i]

                    start_price = None
                    end_price = None
                    for timestamp,price in price_data.items():
                        if int(timestamp) > int(unix_start_time) and start_price is None:
                            start_price = price

                        if int(timestamp) > int(unix_end_time):
                            end_price = price


                    if end_price is None:
                        end_price = price_data[timestamps[-1]]



                    try:

                        diff = end_price - start_price
                        pct_chg = diff/start_price * 100

                        price_changes[site].append({'symbol': symbol, 'pct_chg': pct_chg, 'start_date': start_date.isoformat(), 'end_date': end_date.isoformat(), 'score': score, 'start_price': start_price, 'end_price': end_price})

                    except TypeError as e:
                        pass





    with open('./price_changes.json', 'w') as ofh:
        json.dump(price_changes,ofh)

    return price_changes

def calculate_avg_pct_chg(price_changes, min_scores):
    avg_pct_changes = {}
    for site, performance_list in price_changes.items():
        min_score = min_scores[site]
        sum_pct = 0
        count = 0
        for p in performance_list:
            if p['score'] >= min_score:
                count += 1
                sum_pct += p['pct_chg']
        if count > 9:
            avg = sum_pct/count
        else:
            avg = 0

        avg_pct_changes[site] = {">%s" % min_score: avg}

    return avg_pct_changes




#pchanges = get_price_changes({'zacks':85, 'gurufocus': 95, 'thestreet': 85}, '<')
pchanges = {}
with open('./price_changes.json') as ifh:
    pchanges = json.load(ifh)
result = calculate_avg_pct_chg(pchanges,{'zacks':85, 'gurufocus': 95, 'thestreet': 85})
print(result)






