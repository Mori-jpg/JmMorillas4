from typing import List
try:
    from .sale import Sale
except ImportError:
    from sale import Sale

class SalesCollection:
    def __init__(self, sales: List[Sale]):
        self.sales = sales

    def sales_by_client(self, client_id: int) -> List[Sale]:
        result = []
        for s in self.sales:
            if s.client_id == client_id:
                result.append(s)
        return result

    def total_amount_by_client(self, client_id: int) -> float:
        total = 0.0
        for s in self.sales:
            if s.client_id == client_id:
                total += s.amount
        return total

    def total_amount_by_category(self, category: str) -> float:
        total = 0.0
        for s in self.sales:
            if s.category.lower() == category.lower():
                total += s.amount
        return total

    def average_sale_by_client(self, client_id: int) -> float:
        sales = self.sales_by_client(client_id)
        if not sales:
            return 0.0
        return self.total_amount_by_client(client_id) / len(sales)
