import backtrader as bt

class SMACrossStrategy(bt.Strategy):
    params = (
        ('short_period', 10),  
        ('long_period', 30),   
        ('ticker', 'SH600519'), 
        ('printlog', True),  
    )

    def __init__(self):

        self.sma_short = bt.indicators.SMA(self.data.close, period=self.params.short_period)
        self.sma_long = bt.indicators.SMA(self.data.close, period=self.params.long_period)
        self.crossover = bt.indicators.CrossOver(self.sma_short, self.sma_long)
        self.trade_log = []  

    def next(self):
        if not self.position:
            if self.crossover > 0:  
                self.buy()
                dt = self.datas[0].datetime.date(0)
                self.log(f'{dt} Buy: Price: {self.data.close[0]}')
        elif self.crossover < 0:  
            self.sell()
            dt = self.datas[0].datetime.date(0)
            self.log(f'{dt} Sell: Price: {self.data.close[0]}')

    def log(self, txt, dt=None):
        if self.params.printlog:
            dt = dt or self.datetime.date(0)
            print(f'{dt.isoformat()}, {txt}')  

    def notify_order(self, order):
        if order.status in [order.Completed]:
            order_type = 'buy' if order.isbuy() else 'sell'
            self.trade_log.append({
                'date': self.datas[0].datetime.date(0).isoformat(),
                'type': order_type,
                'symbol': self.params.ticker,
                'price': order.executed.price,
                'size': order.executed.size,
            })
            self.log(f'{order_type.upper()} EXECUTED, Price: {order.executed.price:.2f}, Cost: {order.executed.value:.2f}, Comm {order.executed.comm:.2f}')

    def stop(self):
        self.log(f'Final Value: {self.broker.getvalue()}')

    def get_trade_data(self):

        return self.trade_log
