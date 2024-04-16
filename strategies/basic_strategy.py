import backtrader as bt

class BasicStrategy(bt.Strategy):
    def __init__(self):
        
        self.ma = bt.indicators.MovingAverageSimple(self.data.close, period=15)

    def next(self):
        
        if self.data.close[0] > self.ma[0]:
            if not self.position:
                self.buy()
        elif self.data.close[0] < self.ma[0]:
            if self.position:
                self.sell()