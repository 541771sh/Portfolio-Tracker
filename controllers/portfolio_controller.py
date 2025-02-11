from models.asset import Asset
from models.portfolio import Portfolio
from services.price_fetcher import fetch_current_price
from views.cli_view import CLIView
from views.graph_view import GraphView
import pandas as pd
from services.price_fetcher import fetch_historical_prices
import yfinance as yf

class PortfolioController:
    def __init__(self, portfolio):
        self.portfolio = portfolio

    import yfinance as yf

    def add_asset(self):
        """Automatically determine sector and asset class based on the ticker."""
        ticker = input("Enter ticker: ").upper()

        # Fetch stock data from Yahoo Finance
        stock_info = yf.Ticker(ticker).info

        # Retrieve sector and asset class from Yahoo Finance data
        sector = stock_info.get("sector", "Unknown")
        asset_class = stock_info.get("quoteType", "Stock").capitalize()

        quantity = int(input("Enter quantity: "))
        purchase_price = float(input("Enter purchase price: "))

        asset = Asset(ticker, sector, asset_class, quantity, purchase_price)
        asset.update_price(fetch_current_price(ticker))
        self.portfolio.add_asset(asset)
        print(f"Successfully added {ticker} to portfolio with sector '{sector}' and asset class '{asset_class}'.")

    def edit_asset(self):
        """Allow the user to edit an asset's quantity or purchase price."""
        ticker = input("Enter ticker of asset to edit: ").upper()
        self.portfolio.edit_asset(ticker)

    def remove_asset(self):
        """Allow the user to remove an asset from the portfolio."""
        ticker = input("Enter ticker of asset to remove: ").upper()
        self.portfolio.remove_asset(ticker)
        
    def update_prices(self):
        """Fetch and update the latest available prices for all assets."""
        print("\n Updating asset prices...\n")

        for asset in self.portfolio.assets:
            new_price = fetch_current_price(asset.ticker)
            if new_price is not None:
                print(f" {asset.ticker}: {asset.current_price} → {new_price} ✅")
                asset.update_price(new_price)
            else:
                print(f"Failed to fetch price for {asset.ticker}")

        print("Prices updated.\n")

    def display_portfolio(self):
        """Show portfolio summary"""
        CLIView.display_portfolio(self.portfolio)
        

    def display_portfolio_summary(self):
        """Show portfolio summary including total value and weights."""
        summary = self.portfolio.portfolio_summary()

        if summary is None:
            print("No portfolio data available.")
            return
    
        CLIView.display_portfolio_summary(
            summary["total_value"],
            summary["asset_weights"],
            summary["asset_class_weights"],
            summary["sector_weights"]
        )


    def display_portfolio_performance_graph(self):
        """Show portfolio performance graph"""
        historical_data = {}
        for asset in self.portfolio.assets:
            history = fetch_historical_prices(asset.ticker)
            if history is not None and not history.empty:
                historical_data[asset.ticker] = history

        if not historical_data:
            print(" No historical data available.")
            return

        portfolio_value = pd.DataFrame(historical_data).sum(axis=1)
        GraphView.plot_portfolio_performance(portfolio_value)
        
    def display_asset_graph(self, tickers):
        """Toon een grafiek met de historische en huidige prijs van de opgegeven tickers."""
        price_data = {}
        current_prices = {}

        for ticker in tickers:
            history = fetch_historical_prices(ticker)
            if history is not None and not history.empty:
                price_data[ticker] = history
            else:
                print(f" No historical data available for {ticker}.")
        
            current_prices[ticker] = fetch_current_price(ticker)
            
            if price_data:
                GraphView.plot_asset_prices(price_data, current_prices)
            else:
                print(" No valid historical price data available.")

    def display_risk_metrics(self):
        """Show portfolio Sharpe & Sortino ratio."""
        risk_metrics = self.portfolio.calculate_portfolio_risk_metrics()

        if risk_metrics:
            print(f" Portfolio Risk Analysis:")
            print(f" Sharpe Ratio: {risk_metrics['sharpe_ratio']:.3f}")
            print(f" Sortino Ratio: {risk_metrics['sortino_ratio']:.3f}")
            print(f" Portfolio Volatility: {risk_metrics['volatility']:.3%}")
        else:
            print(" Not enough data to calculate risk metrics.")

    def run_monte_carlo(self):
        """Run Monte Carlo simulation on the portfolio."""
        self.portfolio.monte_carlo_simulation()

    def optimize_portfolio(self):
        """Find the optimal portfolio allocation."""
        self.portfolio.optimize_portfolio()
