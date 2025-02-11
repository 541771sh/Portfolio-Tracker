import yfinance as yf
import pandas as pd
import datetime

def fetch_current_price(ticker):
    """Fetch the most recent market price. Use pre-market price only if market is closed."""
    try:
        stock = yf.Ticker(ticker)
        stock_info = stock.info

        # Get market state (Regular, Pre, Post, Closed)
        market_state = stock_info.get("marketState", "CLOSED").upper()

        # If market is open, get live price
        if market_state in ["REGULAR", "OPEN"]:
            history = stock.history(period="1d", interval="1m")
            if not history.empty:
                latest_price = history["Close"].iloc[-1]
                print(f"Market Open - Using LIVE price for {ticker}: {latest_price}")
                return latest_price

        # If market is closed, get pre-market price
        if market_state in ["PRE", "POST", "CLOSED"]:
            pre_market_price = stock_info.get("preMarketPrice")
            if pre_market_price:
                print(f"Market Closed - Using PRE-MARKET price for {ticker}: {pre_market_price}")
                return pre_market_price

        # If neither live nor pre-market price is available, use last closing price
        history = stock.history(period="5d")  # Fetch last 5 days to avoid missing data
        if not history.empty:
            close_price = history["Close"].dropna().iloc[-1]  # Drop NaN values and get last close
            print(f" No live/pre-market data - Using LAST CLOSE price for {ticker}: {close_price}")
            return close_price

        print(f" No price data available for {ticker}.")
        return None

    except Exception as e:
        print(f" Error fetching price for {ticker}: {e}")
        return None



def fetch_historical_prices(ticker, period="6mo"):
    """Fetch historical prices for a stock over a given period."""
    try:
        stock = yf.Ticker(ticker)
        history = stock.history(period=period)
        return history["Close"]  # Returns closing prices
    except Exception as e:
        print(f"Error fetching historical prices for {ticker}: {e}")
        return None
