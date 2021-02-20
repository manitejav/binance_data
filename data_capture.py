from datetime import datetime
from time import time
import ccxt
import psycopg2



# datetime.fromtimestamp(time/1000)

def insert_5_tickers(exchange, symbol, cur):
    res=exchange.fetch_ticker(symbol)
    SQL =  "INSERT INTO one_tick_data (time, market, open, close, high, low, volume) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    try:
        data = (datetime.fromtimestamp(res['timestamp']/1000), res['symbol'], res['info']['openPrice'], res['info']['lastPrice'], res['info']['highPrice'], res['info']['lowPrice'], res['info']['volume'])
        cur.execute(SQL, data)
    except (Exception, psycopg2.Error) as error:
        print(error.pgerror)

print(ccxt.exchanges)

exchange = ccxt.binance({
    'rateLimit':1000,
    'headers':{
        
    },
    'interval':"1m",
    'options':{
        'adjustedForTimeDifference': True,
    }
})

exchange.load_markets()

symbols = exchange.symbols

# print(exchange.symbols)
# eth1=exchange.fetch_ticker(symbols[0])

# print(eth1)

CONNECTION = "postgres://mani:abcd@localhost:5432/nyc_data"
conn=psycopg2.connect(CONNECTION)
cur = conn.cursor()

for i in range(0,5):
    print(symbols[i])
    insert_5_tickers(exchange, symbols[i], cur)





conn.commit()


query = "SELECT * FROM one_tick_data;"

cur.execute(query)

for i in cur.fetchall():
    print(i)

cur.close()

