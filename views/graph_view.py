import matplotlib.pyplot as plt
import pandas as pd
import datetime

class GraphView:
    @staticmethod
    def plot_asset_prices(price_data, current_prices):
        """Plot historical price data up to the present time with the current price as the latest data point."""
        plt.figure(figsize=(10, 5))

        for ticker, prices in price_data.items():
            if prices is not None and not prices.empty:
                # Convert timezone-aware timestamps to timezone-naive
                prices.index = prices.index.tz_localize(None)

                # Extend historical data with today's price if available
                if ticker in current_prices and current_prices[ticker] is not None:
                    today = pd.Timestamp(datetime.datetime.now().date())  # Current date
                    extended_prices = prices.copy()
                    extended_prices.loc[today] = current_prices[ticker]  # Append current price
                    extended_prices.plot(label=ticker)  # Plot extended prices
                else:
                    prices.plot(label=ticker)  # If no current price, plot normally
            else:
                print(f"⚠️ No historical data available for {ticker}.")

        plt.xlabel("Date")
        plt.ylabel("Price (USD)")
        plt.title("Current & Historical Price Chart")
        plt.legend()
        plt.grid()
        plt.show()

    @staticmethod
    def plot_portfolio_performance(portfolio_value):
        """Plot portfolio value over time."""
        plt.figure(figsize=(10, 5))
        portfolio_value.plot(color='blue', label='Portfolio Value')
        plt.xlabel("Date")
        plt.ylabel("Total Portfolio Value (USD)")
        plt.title("Portfolio Performance Over Time")
        plt.legend()
        plt.grid()
        plt.show()
