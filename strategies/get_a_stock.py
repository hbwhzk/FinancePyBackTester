import requests
from datetime import datetime
import pandas as pd
import backtrader.feeds as btfeeds


def get_a_stock(symbol, start_date, end_date):
    print(f"Fetching data for {symbol} from {start_date} to {end_date}")
    start_dt = datetime.strptime(start_date, '%Y-%m-%d')
    start_ts = int(start_dt.timestamp() * 1000)
    end_dt = datetime.strptime(end_date, '%Y-%m-%d')
    backdays = (end_dt - start_dt).days

    session = requests.Session()
    session.headers.update({"user-agent": "Mozilla/5.0"})
    r = session.get("https://xueqiu.com")
    t = r.cookies.get("xq_a_token")
    data_url = f"https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol={symbol}&begin={start_ts}&period=day&type=before&count={backdays}"
    try:
        response = session.get(data_url, cookies={"xq_a_token": t})

        if response.status_code == 200:
            json_data = response.json()
            df = pd.DataFrame(json_data['data']['item'], columns=json_data['data']['column'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            if not df.empty:
                # print("Data retrieved successfully.")
                # print(df.head())
                # print(df.tail())
                return btfeeds.PandasData(dataname=df), True
    except Exception as e:
        print("Data retrieval failed:", e)
    return None, False




# Example usage
# symbol = 'SZ000002'
# start_date = '2023-10-01'
# end_date = '2024-10-10'

# # 获取数据
# data = get_a_stock(symbol, start_date, end_date)
# print(data)




