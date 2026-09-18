from typing import List
try:
    from .sale import Sale
except ImportError:
    from sale import Sale

# FUNCIONES PURAS - no modifican la lista original

def filter_sales_by_category(sales: List[Sale], category: str) -> List[Sale]:
    return list(filter(lambda s: s.category.lower() == category.lower(), sales))

def filter_sales_by_date_range(sales: List[Sale], start: str, end: str) -> List[Sale]:
    return list(filter(lambda s: start <= s.date <= end, sales))

def map_sales_to_amounts(sales: List[Sale]) -> List[float]:
    return list(map(lambda s: s.amount, sales))

def total_revenue_func(sales: List[Sale]) -> float:
    from functools import reduce
    return reduce(lambda acc, s: acc + s.amount, sales, 0.0)

def filter_clients_by_country_pure(clients, country: str):
    return list(filter(lambda c: c.country.lower() == country.lower(), clients))
