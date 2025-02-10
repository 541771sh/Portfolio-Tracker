class Asset:
    def __init__(self, ticker, sector, asset_class, quantity, purchase_price):
        self.ticker = ticker
        self.sector = sector
        self.asset_class = asset_class
        self.quantity = quantity
        self.purchase_price = purchase_price
        self.current_price = purchase_price  # Default to purchase price if not updated

    def update_price(self, new_price):
        """Update the current market price of the asset."""
        self.current_price = new_price

    def current_value(self):
        """Calculate the total current value of the asset in the portfolio."""
        return self.quantity * self.current_price

    def transaction_value(self):
        """Calculate the original investment value."""
        return self.quantity * self.purchase_price
  