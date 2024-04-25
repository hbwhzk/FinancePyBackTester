import yfinance as yf
import backtrader.feeds as btfeeds

def get_data_from_yahoo(symbol, start_date, end_date):
    print(f"Fetching data for {symbol} from {start_date} to {end_date}")
    data = yf.download(symbol, start=start_date, end=end_date)
    if not data.empty:
        return btfeeds.PandasData(dataname=data), True
    return None, False

