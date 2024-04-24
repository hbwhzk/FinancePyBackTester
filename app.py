from flask import Flask, request, render_template
import backtrader as bt
from strategies.get_a_stock import get_a_stock
from strategies.rsi import RSIStrategy
from strategies.sma import SMACrossStrategy
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def index():
    end_date = datetime.now() - timedelta(days=1)  
    start_date = end_date - timedelta(days=365)  

    
    end_date_str = end_date.strftime('%Y-%m-%d')
    start_date_str = start_date.strftime('%Y-%m-%d')
    return render_template('index.html', start_date=start_date_str, end_date=end_date_str)


@app.route('/results', methods=['GET'])
def results():
    symbol = request.args.get('symbol')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    strategy_name = request.args.get('strategy')
    param1 = int(request.args.get('param1', 14))  
    param2_str = request.args.get('param2', '30')  
    try:
        param2 = int(param2_str) if param2_str.isdigit() else None
    except ValueError:
        param2 = None  

    cerebro = bt.Cerebro()
    start_cash = float(request.args.get('initial_cash', 100000))
    
    
    size = int(request.args.get('size', 100))  
    commission_rate = float(request.args.get('commission', 0.0005))  
    print(f"Commission Rate: {commission_rate}")

    cerebro.broker.set_cash(start_cash)

  
    cerebro.broker.setcommission(commission=commission_rate)
    cerebro.addsizer(bt.sizers.FixedSize, stake=size)

    data, success = get_a_stock(symbol, start_date, end_date)  #
    print("Data retrieval success:", success)
    if not success:
        return "Failed to fetch data for the provided dates.", 500

    cerebro.adddata(data)

    if strategy_name == 'RSI':
        cerebro.addstrategy(RSIStrategy, period=param1)
    elif strategy_name == 'MovingAverageCross' and param2 is not None:
        cerebro.addstrategy(SMACrossStrategy, short_period=param1, long_period=param2)

    cerebro.tradehistory = True  

    strategies = cerebro.run()
    if strategies:
        strategy = strategies[0]  
        if hasattr(strategy, 'get_trade_data'):
            trade_data = strategy.get_trade_data()  
            print("trade data:", trade_data)
        else:
            print("no get_buy_sell_sign method")
            trade_data = []
    else:
        print("no result")
        trade_data = []

    final_value = round(cerebro.broker.getvalue(),2)
    candlestick_data = get_candlestick_data(data)

    return render_template('results.html', initial_cash=start_cash, final_value=final_value, 
                           results={'candlesticks': candlestick_data, 'trades': trade_data})


def get_candlestick_data(datafeed):
    ohlc = []
    for i in range(len(datafeed)):
        date = datafeed.datetime.array[i]
        o = datafeed.open.array[i]
        h = datafeed.high.array[i] 
        l = datafeed.low.array[i]
        c = datafeed.close.array[i]
        v = datafeed.volume.array[i]
        ohlc.append({
            't': bt.num2date(date).strftime('%Y-%m-%d'),
            'o': round(o,2),
            'h': round(h,2),
            'l': round(l,2),
            'c': round(c,2),
            'v': v
        })
    return ohlc




if __name__ == '__main__':
    app.run(debug=True)




