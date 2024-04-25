from Stock import Stock
from Commodity import Commodity
from ETF import ETF
from Fund import Fund
from Bond import Bond
from Portfolio import InvestmentPortfolio
from PositionSizing import PositionSizing
import datetime

if __name__ == '__main__':
    # 定义训练期间
    train_start_date = datetime.datetime(2018, 1, 1)
    train_end_date = datetime.datetime(2019, 1, 1)

    # 训练标的物并记录胜率与赔率
    sizing = PositionSizing(train_start_date, train_end_date)
    sizing.train('600519', 'Stock')
    # sizing.train('SPY', 'ETF')
    # sizing.train('GC=F', 'Commodity')
    # sizing.train('TLT', 'Bond')
    # sizing.train('VFIAX', 'Fund')

    print(sizing['600519'].positionSize)
    print(sizing['600519'].winProb)
    print(sizing['600519'].rateWin)
    print(sizing['600519'].rateLoss)

    # 初始化投资组合，设定初始资本
    initial_capital = 10000
    portfolio = InvestmentPortfolio(initial_capital, sizing)

    # 定义投资期间
    invest_start_date = datetime.datetime(2019, 1, 1)
    invest_end_date = datetime.datetime(2020, 1, 1)

    # 添加不同的投资类型到投资组合
    portfolio.add_investment(Stock('600519', invest_start_date, invest_end_date), initial_capital)
    # portfolio.add_investment(ETF('SPY', invest_start_date, invest_end_date), initial_capital)
    # portfolio.add_investment(Commodity('GC=F', invest_start_date, invest_end_date), initial_capital)
    # portfolio.add_investment(Bond('TLT', invest_start_date, invest_end_date), initial_capital)
    # portfolio.add_investment(Fund('VFIAX', invest_start_date, invest_end_date), initial_capital)

    # 运行整个投资组合
    portfolio.run()

    # 输出整体投资组合的表现
    portfolio.portfolio_performance()

    # 如果需要进一步操作，如重新分配资本等
    portfolio.reallocate_capital()