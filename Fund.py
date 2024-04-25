import numpy as np
from Investment import Investment


class Fund(Investment):
    def __init__(self, ticker, start_date, end_date):
        super().__init__(ticker, start_date, end_date)

    def calculate_indicators(self):
        # 可以根据基金的特性设定指标，这里简单使用动量
        self.data['Momentum'] = self.data['收盘'].pct_change(periods=30) * 100

    def execute_strategy(self):
        # 简单的动量策略
        self.data['Signal'] = 0
        self.data['Signal'] = np.where(self.data['Momentum'] > 0, 1, -1)
        self.data['Position'] = self.data['Signal'].diff()
