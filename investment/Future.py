from Investment import Investment
import akshare as ak


class FuturesInvestment(Investment):
    def __init__(self, symbol, capital=100000):
        super().__init__(symbol)
        self.initial_capital = capital
        self.capital = capital
        self.position_size = 0
        self.active_position = False

    def fetch_data(self, start_date, end_date):
        self.data = ak.futures_zh_daily_sina(symbol=self.symbol)

    def calculate_technical_indicators(self):
        self.data['RSI'] = self.calculate_rsi(self.data['close'], 14)
        self.data['Volatility'] = self.data['close'].rolling(window=10).std()

    def generate_signals(self):
        self.data['Signal'] = 0
        self.data.loc[(self.data['RSI'] > 70) & (
                    self.data['Volatility'] < self.data['Volatility'].rolling(window=10).mean()), 'Signal'] = -1
        self.data.loc[(self.data['RSI'] < 30) & (
                    self.data['Volatility'] < self.data['Volatility'].rolling(window=10).mean()), 'Signal'] = 1
        self.data['Position'] = self.data['Signal'].diff()

    def calculate_rsi(self, prices, n=14):
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=n).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=n).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def simulate_trading(self):
        self.data['Portfolio_value'] = self.capital
        for i, row in self.data.iterrows():
            if row['Position'] > 0 and self.capital > 1:
                # kelly_fraction = self.calculate_kelly_criterion()
                kelly_fraction = 1.0
                position = self.capital * kelly_fraction / row['close']
                self.capital -= position * row['close']
                self.position_size += position
                print(f"buy: {self.capital}, {self.position_size}, {row['close']}")
            elif row['Position'] < 0:
                self.capital += self.position_size * row['close']
                self.position_size = 0
                print(f"sell: {self.capital}, {self.position_size}, {row['close']}")
            self.data.at[i, 'Portfolio_value'] = self.capital + (self.position_size * row['close'])

    def calculate_kelly_criterion(self):
        # 根据每日价格变动计算凯利准则的胜率和盈亏比
        self.data['Daily_Returns'] = self.data['close'].pct_change()
        winning_trades = self.data[self.data['Daily_Returns'] > 0]
        losing_trades = self.data[self.data['Daily_Returns'] < 0]
        if len(winning_trades) == 0 or len(losing_trades) == 0:
            # 防止除以零的情况
            return 0
        win_prob = len(winning_trades) / len(self.data.dropna(subset=['Daily_Returns']))
        win_loss_ratio = winning_trades['Daily_Returns'].mean() / abs(losing_trades['Daily_Returns'].mean())
        # 凯利公式：f = p - (q / b)
        return win_prob - ((1 - win_prob) / win_loss_ratio)

    def backtest_strategy(self):
        self.calculate_technical_indicators()
        self.generate_signals()
        self.simulate_trading()
        return self.data['Portfolio_value'].iloc[-1] / self.initial_capital


# 使用示例
if __name__ == '__main__':
    futures = FuturesInvestment('RB0')  # 示例期货代码
    futures.fetch_data('20200101', '20201231')
    futures.calculate_technical_indicators()
    futures.generate_signals()
    final_return = futures.backtest_strategy()
    print(f'策略最终回报: {final_return}')
