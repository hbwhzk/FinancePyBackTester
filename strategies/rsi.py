import backtrader as bt

class RSIStrategy(bt.Strategy):
    params = (
        ('period', 14),
        ('rsi_low', 30),  
        ('rsi_high', 70),  

        ('printlog', True),  
    )

    def __init__(self):
        self.symbol = self.datas[0]._name
        self.rsi = bt.indicators.RSI(self.data.close, period=self.params.period)
        self.buy_signal = bt.indicators.CrossDown(self.rsi, self.params.rsi_low)  
        self.sell_signal = bt.indicators.CrossOver(self.rsi, self.params.rsi_high)  
        self.trade_log = []  

    def notify_order(self, order):
        if order.status in [order.Completed]:
            cash = self.broker.get_cash()
            value = self.broker.get_value() - cash
            total = self.broker.get_value()
            
            order_type = 'buy' if order.isbuy() else 'sell'
            self.trade_log.append({
                'date': self.datas[0].datetime.date(0).isoformat(),
                'type': order_type,
                'symbol': self.symbol,
                'price': round(order.executed.price, 2),
                'size': order.executed.size,
                'comm': round(order.executed.comm,2),
                'cash': round(cash, 2), 
                'value': round(value,2),
                'total': round(total,2)
            })
            self.log(
                f'{order_type.upper()} EXECUTED, Price: {order.executed.price:.2f}, '
                f'Cost: {order.executed.value:.2f}, Comm {order.executed.comm:.2f}, '
                f'Cash: {cash:.2f}, Value: {value:.2f}, Total: {total:.2f}'
            )

    def log(self, txt, dt=None, trade_type=None, price=None):
        if self.params.printlog:
            dt = dt or self.datetime.date(0)
            log_msg = f'{dt.isoformat()}, {txt}'  
            if trade_type:
                log_msg += f', Trade Type: {trade_type}'
            if price:
                log_msg += f', Price: {price}'
            print(log_msg)

    def next(self):
        if self.buy_signal[0] == 1:  
            self.buy()
            dt = self.datas[0].datetime.date(0)
            self.log('Buy', dt=dt, trade_type='Buy', price=self.data.close[0])
        elif self.sell_signal[0] == 1 and self.position:  # 
            self.sell()
            dt = self.datas[0].datetime.date(0)
            self.log('Sell', dt=dt, trade_type='Sell', price=self.data.close[0])

    def stop(self):
        self.log(f'(Period: {self.params.period}) Final Value: {self.broker.getvalue()}')

    def get_trade_data(self):

        print("Trading logging", self.trade_log)
        return self.trade_log
