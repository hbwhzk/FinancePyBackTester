import requests
from datetime import datetime
import pytz
import yfinance as yf
import pandas as pd
import logging


logging.basicConfig(level=logging.DEBUG, filename='load_data.log', filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def fetch_data_from_yahoo(symbol, start_date, end_date):
    try:
        logging.info(f"Attempting to download data from Yahoo for {symbol}")
        data = yf.download(symbol, start=start_date, end=end_date)
        if data.empty:
            logging.warning(f"No data returned for {symbol} from {start_date} to {end_date}.")
            return None
        

        data.reset_index(inplace=True)
        

        data['Date'] = pd.to_datetime(data['Date'])
        data.set_index('Date', inplace=True)
        

        data.rename(columns={
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume"
        }, inplace=True)

        logging.info(f"Data formatted and ready for use for {symbol}")
        return data
    except Exception as e:
        logging.error(f"Failed to download data for {symbol}: {e}")
        return None

