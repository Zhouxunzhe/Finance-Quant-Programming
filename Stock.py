import numpy as np
import datetime

from Investment import Investment
from TechnicalLib import calculate_SMA


class Stock(Investment):
    def __init__(self, ticker, start_date, end_date):
        super().__init__(ticker, start_date, end_date)

    def calculate_indicators(self):
        # 计算简单移动平均线 (SMA)
        self.data['SMA_20'] = calculate_SMA(self.data, 20)
        self.data['SMA_50'] = calculate_SMA(self.data, 50)

    def execute_strategy(self):
        # 简单的移动平均线交叉策略
        self.data['Signal'] = 0
        self.data['Signal'] = np.where(self.data['SMA_20'] > self.data['SMA_50'], 1, 0)
        self.data['Position'] = self.data['Signal'].diff()

        # 记录交易
        self.trades = self.data[self.data['Position'] != 0]


if __name__ == '__main__':
    start_date = datetime.datetime(2019, 1, 1)
    end_date = datetime.datetime(2020, 1, 1)
    aapl_stock = Stock('600519', start_date, end_date)
    aapl_stock.calculate_indicators()
    aapl_stock.execute_strategy()
    aapl_stock.evaluate_performance(plot=True)
