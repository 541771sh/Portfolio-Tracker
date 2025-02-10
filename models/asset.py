class Asset:
    def __init__(self, ticker, sector, asset_class, quantity, purchase_price):
        self.ticker = ticker
        self.sector = sector
        self.asset_class = asset_class
        self.quantity = quantity
        self.purchase_price = purchase_price
        self.current_price = None  # Default to None

    def transaction_value(self):
        """Calculate the original transaction value"""
        return self.quantity * self.purchase_price

    def current_value(self):
        """Calculate the current value based on latest price"""
        if self.current_price is not None:
            return self.quantity * self.current_price
        return 0  # Default to 0 if current price is not set

    def update_price(self, new_price):
        """Update the asset’s current price"""
        print(f"Setting {self.ticker} price to {new_price}")  # Debugging statement
        self.current_price = new_price  # Ensure update works
