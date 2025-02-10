from models.asset import Asset
from models.portfolio import Portfolio
from services.price_fetcher import fetch_current_price
from views.cli_view import CLIView
import pandas as pd
from services.price_fetcher import fetch_historical_prices
from views.graph_view import GraphView
import yfinance as yf
from models.asset import Asset


class PortfolioController:
    def __init__(self, portfolio):
        self.portfolio = portfolio

    def add_asset(self):
        """Add a new asset, automatically fetching its sector and asset class."""
        ticker = input("Enter ticker: ").upper()
        
        # Fetch sector and asset class from Yahoo Finance
        try:
            stock = yf.Ticker(ticker)
            sector = stock.info.get("sector", "Unknown")
            asset_class = stock.info.get("quoteType", "Stock")  # Usually "EQUITY" for stocks, "ETF", etc.
        except Exception as e:
            print(f"⚠️ Error retrieving data for {ticker}: {e}")
            sector = "Unknown"
            asset_class = "Unknown"

        quantity = int(input("Enter quantity: "))
        purchase_price = float(input("Enter purchase price: "))

        # Create asset object and add it to the portfolio
        asset = Asset(ticker, sector, asset_class, quantity, purchase_price)
        self.portfolio.add_asset(asset)
        print(f"✅ {ticker} added successfully with sector '{sector}' and asset class '{asset_class}'.")

    def edit_asset(self):
        """Allow the user to edit an asset's quantity or purchase price"""
        ticker = input("Enter ticker of asset to edit: ").upper()
        new_quantity = input("Enter new quantity (press Enter to skip): ")
        new_purchase_price = input("Enter new purchase price (press Enter to skip): ")
        
        new_quantity = int(new_quantity) if new_quantity else None
        new_purchase_price = float(new_purchase_price) if new_purchase_price else None
        
        self.portfolio.edit_asset(ticker, new_quantity, new_purchase_price)

    def remove_asset(self):
        """Allow the user to remove an asset from the portfolio"""
        ticker = input("Enter ticker of asset to remove: ").upper()
        self.portfolio.remove_asset(ticker)
        
    def update_prices(self):
        """Fetch and update the current prices for all assets"""
        print("\nUpdating prices...")

        for asset in self.portfolio.assets:
            new_price = fetch_current_price(asset.ticker)
            if new_price is not None:
                print(f"{asset.ticker}: {asset.current_price} → {new_price}")
                asset.update_price(new_price)
            else:
                print(f"Failed to fetch price for {asset.ticker}")

        print("Prices updated.\n")

    def display_portfolio(self):
        """Show portfolio in CLI"""
        CLIView.display_portfolio(self.portfolio)


    def display_portfolio_summary(self):
        """Show total portfolio value, gain/loss, return %, volatility, and Sharpe ratio"""
        summary = self.portfolio.portfolio_summary()
        
        CLIView.display_portfolio_summary(
            summary["total_value"],
            summary["total_gain"],
            summary["return_pct"],
            summary["volatility"],
            summary["sharpe_ratio"],
            summary["asset_weights"],
            summary["class_weights"],
            summary["sector_weights"]
            )

    def display_portfolio_performance_graph(self):
        """Show portfolio performance over time by tracking total value."""
        
        print("\nFetching historical prices for portfolio assets...\n")
        
        historical_data = {}
        
        for asset in self.portfolio.assets:
            history = fetch_historical_prices(asset.ticker, period="6mo")
            if history is not None and not history.empty:
                historical_data[asset.ticker] = history
            else:
                print(f"⚠️ No historical data available for {asset.ticker}")
                
        if not historical_data:
            print("❌ No historical data found. Cannot plot portfolio performance.")
            return

        # Convert historical prices into a DataFrame
        historical_prices_df = pd.DataFrame(historical_data)
        
        # Multiply each price by the respective asset's quantity to get portfolio value per day
        portfolio_value = (historical_prices_df * pd.Series(
            {asset.ticker: asset.quantity for asset in self.portfolio.assets}
        )).sum(axis=1)

        GraphView.plot_portfolio_performance(portfolio_value)
        


    def display_asset_graph(self, tickers):
        """Show the latest current price and plot historical prices."""
        if isinstance(tickers, str):
            tickers = [tickers]  # Convert single ticker to list

        print("\nFetching current prices...\n")
        price_data = {}
        current_prices = {}

        for ticker in tickers:
            current_price = fetch_current_price(ticker)
            if current_price is not None:
                print(f"📈 {ticker} Current Price: ${current_price:.2f}")
                current_prices[ticker] = current_price
            else:
                print(f"⚠️ Could not fetch current price for {ticker}.")
        
            price_data[ticker] = fetch_historical_prices(ticker)  # Get historical prices

        GraphView.plot_asset_prices(price_data, current_prices)

