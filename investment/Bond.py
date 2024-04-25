import akshare as ak
from Investment import Investment

class BondInvestment(Investment):
    def __init__(self, symbol, capital=100000):
        super().__init__(symbol)
        self.initial_capital = capital
        self.capital = capital
        self.position_size = 0

    def fetch_data(self, start_date, end_date):
        # Assuming there's a specific akshare method for bond data; adjust as necessary
        self.data = ak.bond_zh_hs_daily(symbol=self.symbol)

    def calculate_technical_indicators(self):
        # Maintaining the same indicators: SMA and Volatility
        self.data['SMA20'] = self.data['close'].rolling(window=20).mean()
        self.data['Volatility'] = self.data['close'].rolling(window=20).std()

    def generate_signals(self):
        # Generate trade signals based on the technical indicators
        self.data['Signal'] = 0
        self.data.loc[(self.data['close'] > self.data['SMA20']) & (
                    self.data['Volatility'] < self.data['Volatility'].rolling(window=10).mean()), 'Signal'] = 1
        self.data.loc[(self.data['close'] < self.data['SMA20']) | (
                    self.data['Volatility'] > self.data['Volatility'].rolling(window=10).mean()), 'Signal'] = -1
        self.data['Position'] = self.data['Signal'].diff()

    def simulate_trading(self):
        # Simulate trading similar to the ETF, Futures, Options code
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
        # Strategy backtesting
        self.calculate_technical_indicators()
        self.generate_signals()
        self.simulate_trading()
        return self.data['Portfolio_value'].iloc[-1] / self.initial_capital

# Using the example
if __name__ == '__main__':
    bond = BondInvestment('sh010107', capital=100000)  # Example bond symbol
    bond.fetch_data('20200101', '20201231')
    bond.calculate_technical_indicators()
    bond.generate_signals()
    final_return = bond.backtest_strategy()
    print(f'Strategy final return: {final_return}')
