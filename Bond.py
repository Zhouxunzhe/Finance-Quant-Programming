import numpy as np
from Investment import Investment


class Bond(Investment):
    def __init__(self, ticker, start_date, end_date):
        super().__init__(ticker, start_date, end_date)

    def calculate_indicators(self):
        # 计算债券的收益率变动
        self.data['Yield Change'] = self.data['Close'].pct_change(periods=14)

    def execute_strategy(self):
        # 当收益率降低时买入，增加时卖出
        self.data['Signal'] = 0
        self.data['Signal'] = np.where(self.data['Yield Change'] < 0, 1, -1)
        self.data['Position'] = self.data['Signal'].diff()
