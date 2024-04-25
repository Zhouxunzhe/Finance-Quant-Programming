import numpy as np
import datetime

from Investment import Investment
from TechnicalLib import RiskManagement
from TechnicalLib import calculate_RSI


class Commodity(Investment):
    def __init__(self, ticker, start_date, end_date):
        super().__init__(ticker, start_date, end_date)

    def calculate_indicators(self):
        # 计算指标，如RSI（相对强弱指数）
        self.data['RSI'] = calculate_RSI(self.data, 14)  # 使用14天的RSI

    def execute_strategy(self):
        # RSI策略：低于30买入，高于70卖出
        self.data['Signal'] = 0
        self.data['Signal'] = np.where(self.data['RSI'] < 30, 1, np.where(self.data['RSI'] > 70, -1, 0))
        self.data['Position'] = self.data['Signal'].diff()


if __name__ == '__main__':
    start_date = datetime.datetime(2019, 1, 1)
    end_date = datetime.datetime(2020, 1, 1)
    # 初始化资金和风险管理
    risk_manager = RiskManagement(initial_capital=10000, risk_per_trade=0.02)

    # 使用商品期货类
    gold = Commodity('GC=F', start_date, end_date)  # 黄金期货
    gold.calculate_indicators()
    gold.execute_strategy()

    # 假设黄金当前价格为1900美元，止损设为1800美元
    position_size = risk_manager.calculate_position_size(1900, 1800)
    print(f"Position size for gold based on risk management: {position_size} units")
