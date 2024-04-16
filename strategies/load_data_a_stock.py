import pandas as pd
import requests
import time
from datetime import datetime

def utc_to_local(utc_dt):
    return pd.to_datetime(utc_dt, unit='ms').dt.tz_localize('UTC').dt.tz_convert('Asia/Shanghai')


def fetch_a_stock_data(symbol, start_date, backdays):
    start_dt = datetime.strptime(start_date, '%Y-%m-%d')
    start_ts = int(start_dt.timestamp() * 1000)


    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"}
    session = requests.Session()
    session.get("https://xueqiu.com", headers=headers)
    cookies = session.cookies.get_dict()


    url = f"https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol={symbol}&begin={start_ts}&period=day&type=before&count=-{backdays}"
    response = session.get(url, headers=headers, cookies=cookies)
    data = response.json()

    if data.get("error_code") == 0:
        items = data["data"]["item"]
        columns = data["data"]["column"]
        df = pd.DataFrame(items, columns=columns)
        df['date'] = utc_to_local(df['timestamp'])
        df.set_index('date', inplace=True)
        df.drop(['timestamp'], axis=1, inplace=True)
        return df

    return pd.DataFrame() 

