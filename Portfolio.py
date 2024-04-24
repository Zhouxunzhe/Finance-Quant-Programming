from Stock import Stock
from Commodity import Commodity
from ETF import ETF
from Fund import Fund
from Bond import Bond
from Commodity import RiskManagement
import datetime


class InvestmentPortfolio:
    def __init__(self, initial_capital):
        self.initial_capital = initial_capital
        self.investments = []
        self.risk_management = RiskManagement(initial_capital, 0.02)

    def add_investment(self, investment):
        self.investments.append(investment)

    def run(self):
        for investment in self.investments:
            investment.calculate_indicators()
            investment.execute_strategy()
            investment.evaluate_performance()

    def portfolio_performance(self):
        total_return = sum(inv.data['Cumulative Strategy Returns'].iloc[-1] for inv in self.investments if 'Cumulative Strategy Returns' in inv.data.columns)
        print(f"Total Portfolio Performance: {total_return - len(self.investments):.2%}")

    def reallocate_capital(self):
        # 根据每个投资的表现和风险重新分配资本
        # 这是一个示例，实际应用时应更复杂
        pass


if __name__ == '__main__':
    # 初始化投资组合，设定初始资本
    initial_capital = 10000
    portfolio = InvestmentPortfolio(initial_capital)

    # 定义投资期间
    start_date = datetime.datetime(2019, 1, 1)
    end_date = datetime.datetime(2020, 1, 1)

    # 添加不同的投资类型到投资组合
    portfolio.add_investment(Stock('AAPL', start_date, end_date))
    portfolio.add_investment(ETF('SPY', start_date, end_date))
    portfolio.add_investment(Commodity('GC=F', start_date, end_date))
    portfolio.add_investment(Bond('TLT', start_date, end_date))
    portfolio.add_investment(Fund('VFIAX', start_date, end_date))

    # 运行整个投资组合
    portfolio.run()

    # 输出整体投资组合的表现
    portfolio.portfolio_performance()

    # 如果需要进一步操作，如重新分配资本等
    portfolio.reallocate_capital()
