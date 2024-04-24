import numpy as np
import datetime

from Investment import Investment


class Commodity(Investment):
    def __init__(self, ticker, start_date, end_date):
        super().__init__(ticker, start_date, end_date)

    def calculate_indicators(self):
        # 计算指标，如RSI（相对强弱指数）
        self.data['RSI'] = self.calculate_RSI(14)  # 使用14天的RSI

    def calculate_RSI(self, window):
        delta = self.data['Close'].diff()
        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0
        gain = up.rolling(window=window).mean()
        loss = down.abs().rolling(window=window).mean()
        RS = gain / loss
        return 100 - (100 / (1 + RS))

    def execute_strategy(self):
        # RSI策略：低于30买入，高于70卖出
        self.data['Signal'] = 0
        self.data['Signal'] = np.where(self.data['RSI'] < 30, 1, np.where(self.data['RSI'] > 70, -1, 0))
        self.data['Position'] = self.data['Signal'].diff()

    def evaluate_performance(self):
        # 类似股票的表现评估方法
        super().evaluate_performance()


class RiskManagement:
    def __init__(self, initial_capital, risk_per_trade):
        self.initial_capital = initial_capital
        self.risk_per_trade = risk_per_trade

    def calculate_position_size(self, price, stop_loss):
        # 计算可用资金的风险百分比
        risk_amount = self.initial_capital * self.risk_per_trade
        position_size = risk_amount / (price - stop_loss)
        return position_size


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
