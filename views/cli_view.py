from tabulate import tabulate

class CLIView:
    @staticmethod
    def display_portfolio(portfolio):
        """Toont de portefeuille met extra informatie zoals transactie- en huidige waarde."""
        if not portfolio.assets:
            print("❌ No assets in portfolio.")
            return

        print("\n📊 Portfolio Overview:\n")
        headers = ["Ticker", "Sector", "Asset Class", "Quantity", "Purchase Price", "Transaction Value", "Current Value"]
    
        data = [[
            asset.ticker, asset.sector, asset.asset_class, asset.quantity,
            f"${asset.purchase_price:,.2f}", f"${asset.transaction_value():,.2f}", f"${asset.current_value():,.2f}"
            ] for asset in portfolio.assets]

        print(tabulate(data, headers=headers, tablefmt="grid"))

    @staticmethod
    def display_portfolio_summary(total_value, asset_weights, asset_class_weights, sector_weights):
        """Display the portfolio value and relative weights per asset, asset class, and sector."""
        print("\n📈 Portfolio Summary:\n")
        
        print(f"💰 Total Portfolio Value: ${total_value:,.2f}\n")
        
        print("🔹 Asset Weights:")
        if asset_weights:
            print(tabulate([[k, f"{v:.2%}"] for k, v in asset_weights.items()], headers=["Ticker", "Weight"], tablefmt="grid"))
        else:
            print("No asset weight data available.")

        print("\n🔹 Asset Class Weights:")
        if asset_class_weights:
            print(tabulate([[k, f"{v:.2%}"] for k, v in asset_class_weights.items()], headers=["Asset Class", "Weight"], tablefmt="grid"))
        else:
            print("No asset class weight data available.")

        print("\n🔹 Sector Weights:")
        if sector_weights:
            print(tabulate([[k, f"{v:.2%}"] for k, v in sector_weights.items()], headers=["Sector", "Weight"], tablefmt="grid"))
        else:
            print("No sector weight data available.")

