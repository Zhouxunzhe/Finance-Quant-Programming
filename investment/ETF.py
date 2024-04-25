import akshare as ak
from Investment import Investment


class ETFInvestment(Investment):
    def __init__(self, symbol):
        super().__init__(symbol)

    def fetch_data(self, start_date, end_date):
        # 使用akshare的stock_zh_index_daily获取ETF指数数据
        self.data = ak.stock_zh_index_daily(symbol=self.symbol)

    def calculate_technical_indicators(self):
        # 计算MACD指标
        self.data['EMA12'] = self.data['close'].ewm(span=12, adjust=False).mean()
        self.data['EMA26'] = self.data['close'].ewm(span=26, adjust=False).mean()
        self.data['MACD'] = self.data['EMA12'] - self.data['EMA26']
        self.data['Signal'] = self.data['MACD'].ewm(span=9, adjust=False).mean()

    def generate_signals(self):
        # 生成交易信号
        self.data['Position'] = 0
        self.data.loc[self.data['MACD'] > self.data['Signal'], 'Position'] = 1
        self.data.loc[self.data['MACD'] < self.data['Signal'], 'Position'] = -1

    def backtest_strategy(self):
        # 策略回测
        self.data['Returns'] = self.data['close'].pct_change()
        self.data['Strategy_Returns'] = self.data['Returns'] * self.data['Position'].shift(1)
        cumulative_returns = (1 + self.data['Strategy_Returns']).cumprod()
        return cumulative_returns.iloc[-1]


# 使用示例
if __name__ == '__main__':
    etf = ETFInvestment('sz399552')  # 示例ETF指数代码
    etf.fetch_data('2020-01-01', '2020-12-31')
    etf.calculate_technical_indicators()
    etf.generate_signals()
    final_return = etf.backtest_strategy()
    print(f'策略最终回报: {final_return}')
