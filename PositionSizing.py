import numpy as np


class _TargetInfo:
    """记录标的物的胜率与赔率"""
    def __init__(self, winProb, rateWin, rateLoss):
        self.winProb = winProb
        self.rateWin = rateWin
        self.rateLoss = rateLoss
    
    @property
    def positionSize(self):
        """动态计算仓位规模"""
        first = self.winProb/self.rateLoss
        second = (1 - self.winProb)/self.rateWin
        return first - second

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
    def calculatePWL(target):
        """计算胜率和盈亏比"""
        # 胜利次数
        winNum = np.where(target.data['Signal']*target.data['Market Return'] > 0, 1, 0).sum()
        # 行动次数
        actNum = np.where(target.data['Signal'] != 0, 1, 0).sum()
        # 胜率
        winProb = winNum / actNum
        # 平均盈利率
        rateWin = np.where(target.data["Strategy Return"] > 0, target.data["Strategy Return"], 0).mean()
        # 平均亏损率
        rateLoss = np.where(target.data["Strategy Return"] < 0, -target.data["Strategy Return"], 0).mean()
        return winProb, rateWin, rateLoss

    def trainBond(self, ticker):
        from Bond import Bond
        bond = Bond(ticker, self.start_date, self.end_date)
        bond.run()
        winProb, rateWin, rateLoss = self.calculatePWL(bond)
        bondInfo = _TargetInfo(winProb, rateWin, rateLoss)
        self.target[ticker] = bondInfo
    
    def trainCommodity(self, ticker):
        from Commodity import Commodity
        commodity = Commodity(ticker, self.start_date, self.end_date)
        commodity.run()
        winProb, rateWin, rateLoss = self.calculatePWL(commodity)
        commodityInfo = _TargetInfo(winProb, rateWin, rateLoss)
        self.target[ticker] = commodityInfo
    
    def trainETF(self, ticker):
        from ETF import ETF
        etf = ETF(ticker, self.start_date, self.end_date)
        etf.run()
        winProb, rateWin, rateLoss = self.calculatePWL(etf)
        etfInfo = _TargetInfo(winProb, rateWin, rateLoss)
        self.target[ticker] = etfInfo
    
    def trainFund(self, ticker):
        from Fund import Fund
        fund = Fund(ticker, self.start_date, self.end_date)
        fund.run()
        winProb, rateWin, rateLoss = self.calculatePWL(fund)
        fundInfo = _TargetInfo(winProb, rateWin, rateLoss)
        self.target[ticker] = fundInfo
    
    def trainStock(self, ticker):
        from Stock import Stock
        stock = Stock(ticker, self.start_date, self.end_date)
        stock.run()
        winProb, rateWin, rateLoss = self.calculatePWL(stock)
        stockInfo = _TargetInfo(winProb, rateWin, rateLoss)
        self.target[ticker] = stockInfo

    