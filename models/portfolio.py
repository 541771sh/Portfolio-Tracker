import numpy as np
import yfinance as yf

class Portfolio:
    def __init__(self):
        self.assets = []

    def add_asset(self, asset):
        """Add a new asset to the portfolio."""
        self.assets.append(asset)
        print(f"✅ {asset.ticker} added to portfolio with sector '{asset.sector}' and asset class '{asset.asset_class}'.")

    def edit_asset(self, ticker, new_quantity=None, new_purchase_price=None):
        """Edit an asset's quantity or purchase price, allowing selection if duplicates exist"""
        matching_assets = [asset for asset in self.assets if asset.ticker == ticker]
        
        if not matching_assets:
            print(f"⚠️ No asset found with ticker {ticker}.")
            return
        
        if len(matching_assets) == 1:
            asset = matching_assets[0]
        else:
            print(f"\nMultiple entries found for {ticker}:")
            for idx, asset in enumerate(matching_assets, start=1):
                print(f"{idx}. Quantity: {asset.quantity}, Purchase Price: {asset.purchase_price}")

            choice = input("Select which asset to edit (enter number): ")
            if not choice.isdigit() or int(choice) < 1 or int(choice) > len(matching_assets):
                print("⚠️ Invalid selection.")
                return

            asset = matching_assets[int(choice) - 1]

        if new_quantity is not None:
            asset.quantity = new_quantity
        if new_purchase_price is not None:
            asset.purchase_price = new_purchase_price
        print(f"✅ {ticker} updated successfully.")


    def remove_asset(self, ticker):
        """Remove an asset from the portfolio, allowing selection if duplicates exist"""
        matching_assets = [asset for asset in self.assets if asset.ticker == ticker]

        if not matching_assets:
            print(f"⚠️ No asset found with ticker {ticker}.")
            return

        if len(matching_assets) == 1:
            self.assets.remove(matching_assets[0])
        else:
            print(f"\nMultiple entries found for {ticker}:")
            for idx, asset in enumerate(matching_assets, start=1):
                print(f"{idx}. Quantity: {asset.quantity}, Purchase Price: {asset.purchase_price}")

            choice = input("Select which asset to remove (enter number): ")
            if not choice.isdigit() or int(choice) < 1 or int(choice) > len(matching_assets):
                print("⚠️ Invalid selection.")
                return

            self.assets.remove(matching_assets[int(choice) - 1])

        print(f"✅ {ticker} removed from portfolio.")
