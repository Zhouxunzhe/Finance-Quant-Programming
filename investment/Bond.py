import akshare as ak
from Investment import Investment


class BondInvestment(Investment):
    def __init__(self, symbol):
        super().__init__(symbol)

    def fetch_data(self, start_date, end_date):
        # 使用akshare的bond_zh_hs_daily获取债券数据
        self.data = ak.bond_zh_hs_daily(symbol=self.symbol)

    def calculate_technical_indicators(self):
        # 计算技术指标
        self.data['SMA20'] = self.data['close'].rolling(window=20).mean()
        self.data['Volatility'] = self.data['close'].rolling(window=20).std()

    def generate_signals(self):
        # 生成交易信号
        self.data['Signal'] = 0
        self.data.loc[self.data['close'] > self.data['SMA20'], 'Signal'] = 1
        self.data.loc[self.data['close'] < self.data['SMA20'], 'Signal'] = -1
        self.data['Position'] = self.data['Signal'].diff()

    def backtest_strategy(self):
        # 策略回测
        self.data['Returns'] = self.data['close'].pct_change()
        self.data['Strategy_Returns'] = self.data['Returns'] * self.data['Position'].shift(1)
        cumulative_returns = (1 + self.data['Strategy_Returns']).cumprod()
        return cumulative_returns.iloc[-1]


# 使用示例
if __name__ == '__main__':
    bond = BondInvestment('sh010107')  # 示例债券代码
    bond.fetch_data('2020-01-01', '2020-12-31')
    bond.calculate_technical_indicators()
    bond.generate_signals()
    final_return = bond.backtest_strategy()
    print(f'策略最终回报: {final_return}')
