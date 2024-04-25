import akshare as ak
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


class Investment:
    def __init__(self, ticker, start_date, end_date):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.data = self.load_data()

    def load_data(self):
        # 使用tushare获取A股数据
        df = ak.stock_zh_a_hist(symbol=self.ticker, start_date=self.start_date.strftime('%Y%m%d'),
                                end_date=self.end_date.strftime('%Y%m%d'), adjust="")
        df['Date'] = pd.to_datetime(df['日期'])
        df.set_index('Date', inplace=True)
        df.sort_index(inplace=True)
        return df

    def calculate_indicators(self):
        # 使用numpy计算20日和50日的简单移动平均线
        # 计算移动平均但保留与原始数据相同的长度
        close_prices = self.data['收盘'].values
        # 计算SMA
        sma_20 = np.convolve(close_prices, np.ones(20) / 20, mode='valid')
        sma_50 = np.convolve(close_prices, np.ones(50) / 50, mode='valid')
        # 创建与原始数据长度相同的全NaN数组
        full_sma_20 = np.full_like(close_prices, np.nan)
        full_sma_50 = np.full_like(close_prices, np.nan)
        # 将计算得到的SMA值放入全NaN数组的适当位置
        full_sma_20[-len(sma_20):] = sma_20  # 从末端开始填充计算出的SMA值
        full_sma_50[-len(sma_50):] = sma_50
        # 将这些完整长度的数组赋值回DataFrame
        self.data['SMA_20'] = full_sma_20
        self.data['SMA_50'] = full_sma_50

    def execute_strategy(self):
        self.data['Signal'] = 0
        self.data['Signal'] = np.where(self.data['SMA_20'] > self.data['SMA_50'], 1, 0)
        self.data['Position'] = self.data['Signal'].diff()

    def evaluate_performance(self):
        self.data['Market Return'] = self.data['收盘'].pct_change()
        self.data['Strategy Return'] = self.data['Market Return'] * self.data['Signal'].shift(1)
        self.data['Cumulative Market Returns'] = (1 + self.data['Market Return']).cumprod()
        self.data['Cumulative Strategy Returns'] = (1 + self.data['Strategy Return']).cumprod()
        plt.figure(figsize=(10, 5))
        plt.plot(self.data.index, self.data['Cumulative Market Returns'], label='Market Returns')
        plt.plot(self.data.index, self.data['Cumulative Strategy Returns'], label='Strategy Returns')
        plt.legend()
        plt.show()


if __name__ == '__main__':
    investment = Investment('600519', datetime(2019, 1, 1), datetime(2020, 1, 1))
    investment.calculate_indicators()
    investment.execute_strategy()
    investment.evaluate_performance()
