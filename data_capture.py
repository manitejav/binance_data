#!/home/ubuntu/venv/binance/bin/python3

from datetime import datetime
import time
import ccxt
import psycopg2
from psycopg2 import Error
import requests
import json


def insert_data(data, market, cur):
    SQL =  "INSERT INTO one_tick_data (time, market, open, close, high, low, volume) VALUES (date_trunc('minute', TIMESTAMP %s), %s, %s, %s, %s, %s, %s)"
    for res in data:
        timestamp = datetime.fromtimestamp(res[0]/1000)
        row = (timestamp, market, res[1], res[4], res[2], res[3], res[5])
        try:
            cur.execute(SQL, row)
        except (Exception, Error) as error:
            print(error)

def insert_tickers(market, conn, startTime, endTime):
    URL = "https://api.binance.com/api/v3/klines"
    symbol=market.replace("/", "")
    PARAMS = {'symbol':symbol, 'interval':'1m', 'startTime':startTime, 'endTime':endTime}

    try:
        r=requests.get(URL, PARAMS)
        data=r.json()
        if "code" in data and data["code"]==-1121 :
            print("Invalid symbol, %s", symbol)
            return

        cur = conn.cursor()
        insert_data(data, market, cur)
        conn.commit()
        cur.close()
    except requests.exceptions.Timeout:
        insert_tickers(market, conn, startTime, endTime)


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

    conn = None

    try:
        conn=psycopg2.connect(user="mani", password="abcd", host="127.0.0.1", port="5432", database="binance_data")
        for symbol in symbols:
            QUERY = "SELECT time from one_tick_data where market=%s ORDER BY time DESC LIMIT 1"
            data = (symbol,)
            cur = conn.cursor()
            cur.execute(QUERY, data)

            if cur.rowcount==0:
                insert_tickers(symbol, conn, round((time.time()-30*24*60)*1000), round(time.time()*1000))
            else:
                for start_time, in cur:
                    insert_tickers(symbol, conn, round((datetime.timestamp(start_time)+1)*1000), round(time.time()*1000))

    except (Exception, Error) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    main()

