import numpy as np


class _TargetInfo:
    """记录标的物的胜率与赔率"""
    def __init__(self, winProb, RewardRiskRatio):
        self.winProb = winProb
        self.RewardRiskRatio = RewardRiskRatio
    
    @property
    def positionSize(self):
        """动态计算仓位规模"""
        numerator = self.RewardRiskRatio*self.winProb - (1 - self.winProb)
        denominator = self.RewardRiskRatio
        return numerator/denominator

class PositionSizing:
    """训练标的物并记录胜率与赔率"""
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.target = {}

    def __getitem__(self, key):
        return self.target[key]
    
    def train(self, ticker, asset):
        if asset == 'Bond':
            self.trainBond(ticker)
        elif asset == 'Commodity':
            self.trainCommodity(ticker)
        elif asset == 'ETF':
            self.trainETF(ticker)
        elif asset == 'Fund':
            self.trainFund(ticker)
        elif asset == 'Stock':
            self.trainStock(ticker)

    @staticmethod
    def calculateWPRRR(target):
        """计算胜率和盈亏比"""
        # 胜利次数
        winNum = np.where(target.data['Signal']*target.data['Market Return'] > 0, 1, 0).sum()
        # 行动次数
        actNum = np.where(target.data['Signal'] != 0, 1, 0).sum()
        # 胜率
        winProb = winNum / actNum
        # 盈亏比
        RewardRiskRatio = target.data['Cumulative Strategy Returns'].iloc[-1] - 1
        return winProb, RewardRiskRatio

    def trainBond(self, ticker):
        from Bond import Bond
        bond = Bond(ticker, self.start_date, self.end_date)
        bond.run()
        winProb, RewardRiskRatio = self.calculateWPRRR(bond)
        bondInfo = _TargetInfo(winProb, RewardRiskRatio)
        self.target[ticker] = bondInfo
    
    def trainCommodity(self, ticker):
        from Commodity import Commodity
        commodity = Commodity(ticker, self.start_date, self.end_date)
        commodity.run()
        winProb, RewardRiskRatio = self.calculateWPRRR(commodity)
        commodityInfo = _TargetInfo(winProb, RewardRiskRatio)
        self.target[ticker] = commodityInfo
    
    def trainETF(self, ticker):
        from ETF import ETF
        etf = ETF(ticker, self.start_date, self.end_date)
        etf.run()
        winProb, RewardRiskRatio = self.calculateWPRRR(etf)
        etfInfo = _TargetInfo(winProb, RewardRiskRatio)
        self.target[ticker] = etfInfo
    
    def trainFund(self, ticker):
        from Fund import Fund
        fund = Fund(ticker, self.start_date, self.end_date)
        fund.run()
        winProb, RewardRiskRatio = self.calculateWPRRR(fund)
        fundInfo = _TargetInfo(winProb, RewardRiskRatio)
        self.target[ticker] = fundInfo
    
    def trainStock(self, ticker):
        from Stock import Stock
        stock = Stock(ticker, self.start_date, self.end_date)
        stock.run()
        winProb, RewardRiskRatio = self.calculateWPRRR(stock)
        stockInfo = _TargetInfo(winProb, RewardRiskRatio)
        self.target[ticker] = stockInfo

    