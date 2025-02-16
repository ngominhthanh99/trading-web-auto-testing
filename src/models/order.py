class Order:
    def __init__(self, symbol, order_type, units=None, size=None, price=None, stop_loss=None, take_profit=None, expiry=None):
        self.symbol = symbol
        self.order_type = order_type
        self.units = units
        self.size = size
        self.price = price
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.expiry = expiry

        if size is None and units is None:
            raise ValueError("Either 'size' or 'units' must be provided.")

    def to_dict(self):
        return self.__dict__