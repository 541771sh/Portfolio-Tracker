import matplotlib.pyplot as plt
import pandas as pd

class GraphView:
    @staticmethod
    def plot_asset_prices(price_data, current_prices):
        """Plot historical price data with the latest current price."""
        plt.figure(figsize=(10, 5))

        for ticker, prices in price_data.items():
            if prices is not None and not prices.empty:
                prices.index = prices.index.tz_localize(None)
                if ticker in current_prices:
                    today = pd.Timestamp("now").normalize()
                    prices.loc[today] = current_prices[ticker]
                prices.plot(label=ticker)

        plt.xlabel("Date")
        plt.ylabel("Price (USD)")
        plt.title(" Current & Historical Asset Prices")
        plt.legend()
        plt.grid()
        plt.show()

    @staticmethod
    def plot_portfolio_performance(portfolio_value):
        """Plot portfolio value over time."""
        plt.figure(figsize=(10, 5))
        portfolio_value.plot(color='blue', label='Portfolio Value', linewidth=2)
        plt.xlabel("Date")
        plt.ylabel("Total Portfolio Value (USD)")
        plt.title(" Portfolio Performance Over Time")
        plt.legend()
        plt.grid()
        plt.show()
