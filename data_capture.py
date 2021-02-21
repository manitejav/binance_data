from datetime import datetime
import time
import ccxt
import psycopg2
import requests
import json
# import asyncio
# import ccxt.async_support as ccxt

def insert_data(data, market, cur):
    SQL =  "INSERT INTO one_tick_data (time, market, open, close, high, low, volume) VALUES (%s, %s, %s, %s, %s, %s, %s)"

    for res in data:
        row = (datetime.fromtimestamp(res[0]/1000), market, res[1], res[4], res[2], res[3], res[5])
        try:
            print(row)
            cur.execute(SQL, row)
        except (Exception, psycopg2.Error) as error:
            print(error)
            print(data)


def insert_tickers(exchange, market, conn, startTime, endTime):
    URL = "https://api.binance.com/api/v3/klines"
    symbol=market.replace("/", "")
    PARAMS = {'symbol':symbol, 'interval':'1m', 'startTime':startTime, 'endTime':endTime}
    r=requests.get(URL, PARAMS)
    data=r.json()
    if "code" in data and data["code"]==-1121 :
        print("Invalid symbol, %s", symbol)
        return

    cur = conn.cursor()
    insert_data(data, market, cur)
    conn.commit()
    print("INSERTED MARKET")
    cur.close()


def main():

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

    CONNECTION = "postgres://mani:abcd@localhost:5432/nyc_data"

    conn = None

    try:
        conn=psycopg2.connect(CONNECTION)
        for symbol in symbols:
            QUERY = "SELECT time from one_tick_data where market=%s ORDER BY time DESC LIMIT 1"
            data = (symbol,)
            cur = conn.cursor()
            cur.execute(QUERY, data)

            if cur.rowcount==0:
                insert_tickers(exchange, symbol, conn, round((time.time()-1000000)*1000), round(time.time()*1000))
            else:
                for start_time, in cur:
                    insert_tickers(exchange, symbol, conn, round(datetime.timestamp(start_time)), round(time.time()*1000))

    except (Exception, psycopg2.Error) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    main()

