import akshare as ak
from Investment import Investment


class FundInvestment(Investment):
    def __init__(self, symbol):
        super().__init__(symbol)

    def fetch_data(self, start_date, end_date):
        # 使用akshare的fund_etf_hist_sina获取基金数据
        self.data = ak.fund_etf_hist_sina(symbol=self.symbol)

    def calculate_technical_indicators(self):
        # 计算技术指标，例如移动平均线和波动率
        self.data['SMA20'] = self.data['close'].rolling(window=20).mean()
        self.data['Volatility'] = self.data['close'].rolling(window=20).std()

    def generate_signals(self):
        # 生成交易信号
        self.data['Signal'] = 0
        self.data.loc[(self.data['close'] > self.data['SMA20']) & (
                    self.data['Volatility'] < self.data['Volatility'].rolling(window=10).mean()), 'Signal'] = 1
        self.data.loc[(self.data['close'] < self.data['SMA20']) | (
                    self.data['Volatility'] > self.data['Volatility'].rolling(window=10).mean()), 'Signal'] = -1
        self.data['Position'] = self.data['Signal'].diff()

    def backtest_strategy(self):
        # 策略回测
        self.data['Returns'] = self.data['close'].pct_change()
        self.data['Strategy_Returns'] = self.data['Returns'] * self.data['Position'].shift(1)
        cumulative_returns = (1 + self.data['Strategy_Returns']).cumprod()
        return cumulative_returns.iloc[-1]


# 使用示例
if __name__ == '__main__':
    fund = FundInvestment('sz169103')  # 示例基金代码
    fund.fetch_data('20200101', '20201231')
    fund.calculate_technical_indicators()
    fund.generate_signals()
    final_return = fund.backtest_strategy()
    print(f'策略最终回报: {final_return}')
