from Investment import Investment
import akshare as ak


class FuturesInvestment(Investment):
    def __init__(self, symbol):
        super().__init__(symbol)

    def fetch_data(self, start_date, end_date):
        # 使用akshare的futures_zh_daily_sina获取期货数据
        self.data = ak.futures_zh_daily_sina(symbol=self.symbol)

    def calculate_technical_indicators(self):
        # 计算RSI和波动率
        self.data['RSI'] = self.calculate_rsi(self.data['close'], 14)
        self.data['Volatility'] = self.data['close'].rolling(window=10).std()

    def generate_signals(self):
        # 生成交易信号
        self.data['Signal'] = 0
        # 超买信号
        self.data.loc[(self.data['RSI'] > 70) & (self.data['Volatility'] < self.data['Volatility'].rolling(window=10).mean()), 'Signal'] = 1
        # 超卖信号
        self.data.loc[(self.data['RSI'] < 30) & (self.data['Volatility'] < self.data['Volatility'].rolling(window=10).mean()), 'Signal'] = -1
        self.data['Position'] = self.data['Signal'].diff()

    def calculate_rsi(self, prices, n=14):
        # 计算RSI值
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=n).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=n).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def backtest_strategy(self):
        # 策略回测
        self.data['Returns'] = self.data['close'].pct_change()
        self.data['Strategy_Returns'] = self.data['Returns'] * self.data['Position'].shift(1)
        cumulative_returns = (1 + self.data['Strategy_Returns']).cumprod()
        return cumulative_returns.iloc[-1]


# 使用示例
if __name__ == '__main__':
    futures = FuturesInvestment('RB0')  # 示例期货代码
    futures.fetch_data('20200101', '20201231')
    futures.calculate_technical_indicators()
    futures.generate_signals()
    final_return = futures.backtest_strategy()
    print(f'策略最终回报: {final_return}')
