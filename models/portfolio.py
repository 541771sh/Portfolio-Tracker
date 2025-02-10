import numpy as np
import yfinance as yf
from collections import Counter

class Portfolio:
    def __init__(self):
        self.assets = []

    def add_asset(self, asset):
        """Add a new asset to the portfolio, automatically fetching its current value"""
        asset.update_price(yf.Ticker(asset.ticker).history(period="1d")['Close'].iloc[-1])
        self.assets.append(asset)

    def total_value(self):
        """Calculate total portfolio value (sum of current values of all assets)"""
        return sum(asset.current_value() for asset in self.assets)

    def total_initial_investment(self):
        """Calculate the total amount originally spent"""
        return sum(asset.transaction_value() for asset in self.assets)

    def total_gain_loss(self):
        """Calculate total portfolio gain/loss"""
        return self.total_value() - self.total_initial_investment()

    def portfolio_return(self):
        """Calculate total portfolio return (%)"""
        initial = self.total_initial_investment()
        if initial == 0:
            return 0
        return (self.total_gain_loss() / initial) * 100

    def asset_weights(self):
        """Calculate relative weights of each asset, properly aggregating duplicate tickers."""
        total = self.total_value()
        if total == 0:
            return {}

        aggregated_assets = Counter()
        for asset in self.assets:
            aggregated_assets[asset.ticker] += asset.current_value()

        return {ticker: value / total for ticker, value in aggregated_assets.items()}

    def asset_class_weights(self):
        """Calculate weight per asset class"""
        total = self.total_value()
        if total == 0:
            return {}

        distribution = {}
        for asset in self.assets:
            if asset.asset_class not in distribution:
                distribution[asset.asset_class] = 0
            distribution[asset.asset_class] += asset.current_value()

        return {k: v / total for k, v in distribution.items()}

    def sector_weights(self):
        """Calculate weight per sector"""
        total = self.total_value()
        if total == 0:
            return {}

        distribution = {}
        for asset in self.assets:
            if asset.sector not in distribution:
                distribution[asset.sector] = 0
            distribution[asset.sector] += asset.current_value()

        return {k: v / total for k, v in distribution.items()}
    
    def portfolio_summary(self):
        """Return all summary calculations as a dictionary"""
        return {
            "total_value": self.total_value(),
            "total_gain": self.total_gain_loss(),
            "return_pct": self.portfolio_return(),
            "asset_weights": self.asset_weights(),
            "class_weights": self.asset_class_weights(),
            "sector_weights": self.sector_weights(),
            "volatility": self.portfolio_volatility(),
            "sharpe_ratio": self.sharpe_ratio()
        }
    
    def portfolio_volatility(self):
        """Calculate portfolio volatility using historical data"""
        returns = []
        for asset in self.assets:
            history = yf.Ticker(asset.ticker).history(period="1mo")['Close'].pct_change().dropna()
            if not history.empty:
                returns.append(history.std())
        return np.mean(returns) if returns else 0
    
    def sharpe_ratio(self, risk_free_rate=0.03):
        """Calculate Sharpe Ratio"""
        volatility = self.portfolio_volatility()
        if volatility == 0:
            return 0  # Avoid division by zero
        return (self.portfolio_return() - (risk_free_rate * 100)) / (volatility * 100)
