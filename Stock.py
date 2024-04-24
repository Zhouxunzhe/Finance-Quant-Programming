import numpy as np
import datetime
from matplotlib import pyplot as plt

from Investment import Investment


class Stock(Investment):
    def __init__(self, ticker, start_date, end_date):
        super().__init__(ticker, start_date, end_date)

    def calculate_indicators(self):
        # 计算简单移动平均线 (SMA)
        self.data['SMA_20'] = self.data['Close'].rolling(window=20).mean()
        self.data['SMA_50'] = self.data['Close'].rolling(window=50).mean()

    def execute_strategy(self):
        # 简单的移动平均线交叉策略
        self.data['Signal'] = 0
        self.data['Signal'][20:] = np.where(self.data['SMA_20'][20:] > self.data['SMA_50'][20:], 1, 0)
        self.data['Position'] = self.data['Signal'].diff()

        # 记录交易
        self.trades = self.data[self.data['Position'] != 0]

    def evaluate_performance(self):
        # 计算投资回报率
        self.data['Market Return'] = self.data['Close'].pct_change()
        self.data['Strategy Return'] = self.data['Market Return'] * self.data['Signal'].shift(1)
        self.data['Cumulative Market Returns'] = (1 + self.data['Market Return']).cumprod()
        self.data['Cumulative Strategy Returns'] = (1 + self.data['Strategy Return']).cumprod()

        # 绘制收益曲线
        plt.figure(figsize=(10,5))
        plt.plot(self.data['Cumulative Market Returns'], label='Market Returns')
        plt.plot(self.data['Cumulative Strategy Returns'], label='Strategy Returns')
        plt.legend()
        plt.show()

        # 总体策略评估
        total_market_return = self.data['Cumulative Market Returns'].iloc[-1]
        total_strategy_return = self.data['Cumulative Strategy Returns'].iloc[-1]
        print(f"Market Return: {total_market_return - 1:.2%}")
        print(f"Strategy Return: {total_strategy_return - 1:.2%}")

if __name__ == '__main__':
    start_date = datetime.datetime(2019, 1, 1)
    end_date = datetime.datetime(2020, 1, 1)
    aapl_stock = Stock('AAPL', start_date, end_date)
    aapl_stock.calculate_indicators()
    aapl_stock.execute_strategy()
    aapl_stock.evaluate_performance()
