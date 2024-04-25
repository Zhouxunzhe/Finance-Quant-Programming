import akshare as ak
from Investment import Investment

class OptionsInvestment(Investment):
    def __init__(self, symbol, capital=100000):
        super().__init__(symbol)
        self.initial_capital = capital
        self.capital = capital
        self.position_size = 0

    def fetch_data(self, start_date, end_date):
        # 使用akshare获取期权数据
        self.data = ak.option_cffex_sz50_daily_sina(symbol=self.symbol)

    def calculate_technical_indicators(self):
        # 计算RSI
        self.data['RSI'] = self.calculate_rsi(self.data['close'], 14)

    def generate_signals(self):
        # 生成交易信号
        self.data['Signal'] = 0
        self.data.loc[self.data['RSI'] > 70, 'Signal'] = -1  # 看跌
        self.data.loc[self.data['RSI'] < 30, 'Signal'] = 1  # 看涨
        self.data['Position'] = self.data['Signal'].diff()

    def calculate_rsi(self, prices, n=14):
        # 计算RSI值
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=n).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=n).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def simulate_trading(self):
        # 模拟交易
        self.data['Portfolio_value'] = self.capital
        for i, row in self.data.iterrows():
            if row['Position'] > 0 and self.capital > 1:
                position = self.capital / row['close']
                self.capital -= position * row['close']
                self.position_size += position
                print(f"buy: {self.capital}, {self.position_size}, {row['close']}")
            elif row['Position'] < 0 and self.position_size > 0:
                self.capital += self.position_size * row['close']
                self.position_size = 0
                print(f"sell: {self.capital}, {self.position_size}, {row['close']}")
            self.data.at[i, 'Portfolio_value'] = self.capital + (self.position_size * row['close'])

    def backtest_strategy(self):
        # 策略回测
        self.calculate_technical_indicators()
        self.generate_signals()
        self.simulate_trading()
        return self.data['Portfolio_value'].iloc[-1] / self.initial_capital

# 使用示例
if __name__ == '__main__':
    options = OptionsInvestment('ho2303P2350')  # 示例期权代码
    options.fetch_data('2020-01-01', '2020-12-31')
    options.calculate_technical_indicators()
    options.generate_signals()
    final_return = options.backtest_strategy()
    print(f'策略最终回报: {final_return}')
