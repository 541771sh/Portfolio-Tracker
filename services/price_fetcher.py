import yfinance as yf
import pandas as pd


def fetch_current_price(ticker):
    """Fetch the real-time intraday price (5-minute interval)."""
    try:
        stock = yf.Ticker(ticker)
        history = stock.history(period="1d", interval="5m")  # 5-minute interval
        return history["Close"].iloc[-1]  # Most recent price
    except Exception as e:
        print(f"Error fetching price for {ticker}: {e}")
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
