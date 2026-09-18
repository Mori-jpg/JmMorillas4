class Sale:
    """Representa una venta"""
    def __init__(self, sale_id, client_id, product, category, amount, date):
        self.sale_id = sale_id  # puede ser S1001
        self.client_id = int(client_id)
        self.product = product
        self.category = category
        self.amount = float(amount)
        self.date = date

    def to_dict(self):
        return {
            "sale_id": self.sale_id,
            "client_id": self.client_id,
            "product": self.product,
            "category": self.category,
            "amount": self.amount,
            "date": self.date
        }
