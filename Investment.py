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
        # 使用pandas_datareader从Yahoo Finance加载数据
        import pandas_datareader as pdr
        return pdr.get_data_yahoo(self.ticker, self.start_date, self.end_date)
        # # 使用tushare获取A股数据
        # df = ak.stock_zh_a_hist(symbol=self.ticker, start_date=self.start_date.strftime('%Y%m%d'),
        #                         end_date=self.end_date.strftime('%Y%m%d'), adjust="")
        # df['Date'] = pd.to_datetime(df['日期'])
        # df.set_index('Date', inplace=True)
        # df.sort_index(inplace=True)
        # return df
    
    def run(self, result=False, plot=False):
        self.calculate_indicators()
        self.execute_strategy()
        self.evaluate_performance(result=result, plot=plot)

    def calculate_indicators(self):
        pass

    def execute_strategy(self):
        pass

    def evaluate_performance(self, result=False, plot=False):
        """评估投资的总体表现"""
        # 计算投资回报率
        self.data['Market Return'] = self.data['Close'].pct_change()
        self.data['Strategy Return'] = self.data['Market Return'] * self.data['Signal'].shift(1)
        self.data['Cumulative Market Returns'] = (1 + self.data['Market Return']).cumprod()
        self.data['Cumulative Strategy Returns'] = (1 + self.data['Strategy Return']).cumprod()

        # 绘制收益曲线
        if plot:
            plt.figure(figsize=(10,5))
            plt.plot(self.data['Cumulative Market Returns'], label='Market Returns')
            plt.plot(self.data['Cumulative Strategy Returns'], label='Strategy Returns')
            plt.legend()
            plt.show()

        # 总体策略评估
        if result or plot:
            total_market_return = self.data['Cumulative Market Returns'].iloc[-1]
            total_strategy_return = self.data['Cumulative Strategy Returns'].iloc[-1]
            print(f"Market Return: {total_market_return - 1:.2%}")
            print(f"Strategy Return: {total_strategy_return - 1:.2%}")
