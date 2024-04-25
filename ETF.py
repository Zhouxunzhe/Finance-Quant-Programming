import numpy as np
from Investment import Investment


class ETF(Investment):
    def __init__(self, ticker, start_date, end_date):
        super().__init__(ticker, start_date, end_date)

    def calculate_indicators(self):
        # 计算动量指标
        self.data['Momentum'] = self.data['收盘'].pct_change(periods=14) * 100

    def execute_strategy(self):
        # 动量策略：当动量正时买入，动量负时卖出
        self.data['Signal'] = 0
        self.data['Signal'] = np.where(self.data['Momentum'] > 0, 1, -1)
        self.data['Position'] = self.data['Signal'].diff()



