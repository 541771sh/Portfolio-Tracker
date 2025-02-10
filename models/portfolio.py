import numpy as np
import yfinance as yf
from collections import Counter
from tabulate import tabulate

class Portfolio:
    def __init__(self):
        self.assets = []

    def add_asset(self, asset):
        """Add a new asset to the portfolio, automatically fetching its current value"""
        try:
            stock = yf.Ticker(asset.ticker)
            price_history = stock.history(period="1d").get("Close")
            
            if price_history is not None and not price_history.empty:
                latest_price = price_history.iloc[-1]
                asset.update_price(latest_price)
            else:
                latest_price = asset.purchase_price  # Default to purchase price
                print(f"⚠️ No recent market data for {asset.ticker}. Using purchase price.")

        except Exception as e:
            latest_price = asset.purchase_price  # Default to purchase price if error occurs
            print(f"⚠️ Error fetching price for {asset.ticker}: {e}")

        self.assets.append(asset)
        print(f"✅ Successfully added {asset.ticker} with price ${latest_price:.2f}\n")

    def display_portfolio(self):
        """Display the portfolio with transaction value before current value"""
        if not self.assets:
            print("❌ No assets in portfolio.")
            return

        print("\n📊 Portfolio Overview:")

        # Debugging: Print transaction values directly
        for asset in self.assets:
            print(f"Debug: {asset.ticker} - Transaction Value: ${asset.transaction_value():,.2f}")
            
            headers = ["Ticker", "Sector", "Asset Class", "Quantity", "Purchase Price", "Transaction Value", "Current Value"]
    
        data = [[
            asset.ticker, 
            asset.sector, 
            asset.asset_class, 
            str(asset.quantity),  # Ensure it's a string
            f"${asset.purchase_price:,.2f}",  
            f"${asset.transaction_value():,.2f}",  # Ensure it's formatted properly
            f"${asset.current_value():,.2f}"
            ] for asset in self.assets]

        print(tabulate(data, headers=headers, tablefmt="grid"))


    def edit_asset(self, ticker, new_quantity=None, new_purchase_price=None):
        """Edit an existing asset's quantity or purchase price, handling duplicates."""
        matching_assets = [asset for asset in self.assets if asset.ticker == ticker]
    
        if not matching_assets:
            print(f"❌ No assets found with ticker {ticker}.")
            return

        # If multiple assets exist, ask the user which one to edit
        if len(matching_assets) > 1:
            print(f"🔹 Multiple assets found for {ticker}. Select which to edit:")
            for i, asset in enumerate(matching_assets):
                print(f"[{i + 1}] Quantity: {asset.quantity}, Purchase Price: ${asset.purchase_price:.2f}, Transaction Value: ${asset.transaction_value():,.2f}")
        
            try:
                choice = input("Enter the number of the asset to edit: ")
                if not choice.isdigit() or not (1 <= int(choice) <= len(matching_assets)):
                    print("❌ Invalid selection.")
                    return
            except ValueError:
                print ("Invalid input")
                return
            
            asset_to_edit = matching_assets[int(choice) - 1]
        else:
            asset_to_edit = matching_assets[0]

        # Ask the user for new values **after selecting the correct asset**
        new_quantity = input("Enter new quantity (press Enter to skip): ")
        new_purchase_price = input("Enter new purchase price (press Enter to skip): ")

        if new_quantity:
            asset_to_edit.quantity = int(new_quantity)
        if new_purchase_price:
            asset_to_edit.purchase_price = float(new_purchase_price)

        print(f"✅ Updated {ticker}: Quantity = {asset_to_edit.quantity}, Purchase Price = ${asset_to_edit.purchase_price:.2f}, Transaction Value = ${asset_to_edit.transaction_value():,.2f}")
    
    def remove_asset(self, ticker):
        """Remove an asset from the portfolio, handling duplicates."""
        matching_assets = [asset for asset in self.assets if asset.ticker == ticker]
    
        if not matching_assets:
            print(f"❌ No assets found with ticker {ticker}.")
            return

        # If multiple assets exist, ask the user which one to remove
        if len(matching_assets) > 1:
            print(f"🔹 Multiple assets found for {ticker}. Select which to remove:")
            for i, asset in enumerate(matching_assets):
                print(f"[{i + 1}] Quantity: {asset.quantity}, Purchase Price: ${asset.purchase_price:.2f}, Transaction Value: ${asset.transaction_value():,.2f}")

            choice = input("Enter the number of the asset to remove: ")
            if not choice.isdigit() or not (1 <= int(choice) <= len(matching_assets)):
                print("❌ Invalid selection.")
                return
            asset_to_remove = matching_assets[int(choice) - 1]
            self.assets.remove(asset_to_remove)
        else:
            self.assets.remove(matching_assets[0])

        print(f"✅ Removed {ticker} from the portfolio.")

    def portfolio_summary(self):
        """Calculate total portfolio value and weights per asset, asset class, and sector."""
        if not self.assets:
            return None  # No data available

        total_value = sum(asset.current_value() for asset in self.assets)

        # 1️⃣ Calculate **asset weights**, grouping multiple assets with the same ticker
        asset_values = {}
        for asset in self.assets:
            asset_values[asset.ticker] = asset_values.get(asset.ticker, 0) + asset.current_value()
        asset_weights = {ticker: value / total_value for ticker, value in asset_values.items()}

        # 2️⃣ Calculate **asset class weights**
        asset_class_values = {}
        for asset in self.assets:
            asset_class_values[asset.asset_class] = asset_class_values.get(asset.asset_class, 0) + asset.current_value()
        asset_class_weights = {k: v / total_value for k, v in asset_class_values.items()}

        # 3️⃣ Calculate **sector weights**, grouping multiple assets in the same sector
        sector_values = {}
        for asset in self.assets:
            sector_values[asset.sector] = sector_values.get(asset.sector, 0) + asset.current_value()
        sector_weights = {k: v / total_value for k, v in sector_values.items()}

        return {
            "total_value": total_value,
            "asset_weights": asset_weights,
            "asset_class_weights": asset_class_weights,
            "sector_weights": sector_weights
        }
