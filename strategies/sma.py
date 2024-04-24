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
                self.log('BUY EXECUTED', dt, trade_type='Buy', price=self.data.close[0])
        elif self.crossover < 0:  
            self.sell()
            dt = self.datas[0].datetime.date(0)
            self.log('SELL EXECUTED', dt, trade_type='Sell', price=self.data.close[0])

    def log(self, txt, dt=None, trade_type=None, price=None):

        if self.params.printlog:
            dt = dt or self.datetime.date(0)
            log_msg = f'{dt.isoformat()}, {txt}'
            if trade_type:
                log_msg += f', Trade Type: {trade_type}'
            if price:
                log_msg += f', Price: {price:.2f}'
            print(log_msg)

    def notify_order(self, order):
        if order.status in [order.Completed]:
            cash = self.broker.get_cash()
            value = self.broker.get_value() - cash
            total = self.broker.get_value()

            order_type = 'buy' if order.isbuy() else 'sell'
            self.trade_log.append({
                'date': self.datas[0].datetime.date(0).isoformat(),
                'type': order_type,
                'symbol': self.params.ticker,
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

    def stop(self):
        self.log(f'(Period: {self.params.short_period}/{self.params.long_period}) Final Value: {self.broker.getvalue()}')

    def get_trade_data(self):
        """
        返回交易记录。
        """
        print("交易记录：", self.trade_log)
        return self.trade_log




# if __name__ == "__main__":
#     cerebro = bt.Cerebro()
#     data = get_a_stock('SZ000002', '2023-10-01', '2024-10-10')
#     if data is not None:
#         cerebro.adddata(data)
#         cerebro.addstrategy(SMACrossStrategy)
#         print("Starting Portfolio Value: %.2f" % cerebro.broker.getvalue())
#         cerebro.run()
#         print("Final Portfolio Value: %.2f" % cerebro.broker.getvalue())
#     else:
#         print("Failed to fetch data.")