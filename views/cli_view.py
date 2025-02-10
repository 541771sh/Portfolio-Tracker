from tabulate import tabulate

class CLIView:
    @staticmethod
    def display_portfolio(portfolio):
        """Display portfolio details in a table."""
        data = []
        for asset in portfolio.assets:
            data.append([
                asset.ticker, asset.sector, asset.asset_class,
                asset.quantity, asset.purchase_price,
                asset.transaction_value(),
                asset.current_value()
            ])
        
        headers = ["Ticker", "Sector", "Asset Class", "Quantity", "Buy Price", "Txn Value", "Current Value"]
        print(tabulate(data, headers=headers, tablefmt="grid"))

    @staticmethod
    def display_portfolio_summary(total_value, total_gain, return_pct, volatility, sharpe, asset_weights, class_weights, sector_weights):
        """Display full portfolio summary with additional metrics."""
        print(f"\n💰 Total Portfolio Value: ${total_value:,.2f}")
        print(f"📈 Total Gain/Loss: ${total_gain:,.2f}")
        print(f"📊 Portfolio Return: {return_pct:.2f}%")
        print(f"⚠️ Portfolio Volatility: {volatility:.4f}")
        print(f"📏 Sharpe Ratio: {sharpe:.2f}\n")

        print("📊 Asset Weights:")
        asset_table = [[ticker, f"{weight*100:.2f}%"] for ticker, weight in asset_weights.items()]
        print(tabulate(asset_table, headers=["Ticker", "Weight"], tablefmt="grid"))

        print("\n🏢 Asset Class Weights:")
        class_table = [[aclass, f"{weight*100:.2f}%"] for aclass, weight in class_weights.items()]
        print(tabulate(class_table, headers=["Asset Class", "Weight"], tablefmt="grid"))

        print("\n🏦 Sector Weights:")
        sector_table = [[sector, f"{weight*100:.2f}%"] for sector, weight in sector_weights.items()]
        print(tabulate(sector_table, headers=["Sector", "Weight"], tablefmt="grid"))

        print("\n")
