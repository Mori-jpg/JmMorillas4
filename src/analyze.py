import json
import csv
import os
import sys

# Compatibilidad: funciona como python src/analyze.py y como pytest
try:
    from .client import Client
    from .sale import Sale
    from .client_collection import ClientCollection
    from .sales_collection import SalesCollection
    from . import functional_utils as fu
except ImportError:
    from client import Client
    from sale import Sale
    from client_collection import ClientCollection
    from sales_collection import SalesCollection
    import functional_utils as fu

import pandas as pd
from collections import defaultdict

def load_data(clients_path, sales_path):
    with open(clients_path, "r", encoding="utf-8") as f:
        clients_raw = json.load(f)
    clients = [Client(c["client_id"], c["name"], c["country"], c["signup_date"]) for c in clients_raw]
    sales = []
    with open(sales_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sales.append(Sale(row["sale_id"], row["client_id"], row["product"], row["category"], row["amount"], row["date"]))
    return clients, sales

def generate_report():
    # Detecta donde se ejecuta
    if os.path.exists("data/clients.json"):
        c_path, s_path, out_path = "data/clients.json", "data/sales.csv", "final_report.json"
    elif os.path.exists("../data/clients.json"):
        c_path, s_path, out_path = "../data/clients.json", "../data/sales.csv", "../final_report.json"
    else:
        c_path = "vscode_proyecto/data/clients.json"
        s_path = "vscode_proyecto/data/sales.csv"
        out_path = "final_report.json"

    clients, sales = load_data(c_path, s_path)
    client_col = ClientCollection(clients)
    sales_col = SalesCollection(sales)

    # 1. total_clients
    total_clients = len(clients)
    # 2. total_sales
    total_sales = len(sales)

    # 3,4,5 - por cliente
    clients_report = []
    for c in clients:
        total_spent = sales_col.total_amount_by_client(c.client_id)
        sale_count = len(sales_col.sales_by_client(c.client_id))
        avg = sales_col.average_sale_by_client(c.client_id)
        clients_report.append({
            "client_id": c.client_id,
            "name": c.name,
            "total_spent": round(total_spent, 2),
            "sale_count": sale_count,
            "average_sale": round(avg, 2)
        })

    total_revenue = fu.total_revenue_func(sales)

    # 6. top_client_by_country
    top_client_by_country = {}
    for country in set(c.country for c in clients):
        clients_in_country = client_col.clients_by_country(country)
        top_client = None
        max_spent = -1
        for cl in clients_in_country:
            spent = sales_col.total_amount_by_client(cl.client_id)
            if spent > max_spent:
                max_spent = spent
                top_client = cl
        if top_client:
            top_client_by_country[country] = top_client.name

    # 7. sales_by_category + 10. monthly_sales con Pandas
    df = pd.DataFrame([s.to_dict() for s in sales])
    sales_by_category = {}
    monthly_sales = {}
    if not df.empty:
        sales_by_category = {k: round(float(v),2) for k,v in df.groupby("category")["amount"].sum().items()}
        df["date"] = pd.to_datetime(df["date"])
        df["month"] = df["date"].dt.to_period("M").astype(str)
        monthly_sales = {k: round(float(v),2) for k,v in df.groupby("month")["amount"].sum().items()}

    # 9. high_spending_clients
    threshold = 500
    high_spending_clients = [c.name for c in clients if sales_col.total_amount_by_client(c.client_id) > threshold]

    final_report = {
        "summary": {
            "total_clients": total_clients,
            "total_sales": total_sales,
            "total_revenue": round(total_revenue,2)
        },
        "clients": clients_report,
        "top_client_by_country": top_client_by_country,
        "sales_by_category": sales_by_category,
        "high_spending_clients": high_spending_clients,
        "monthly_sales": monthly_sales
    }

    with open(out_path, "w", encoding="utf-8") as out:
        json.dump(final_report, out, indent=2, ensure_ascii=False)

    print(f"✅ Informe generado en {out_path}")
    print(json.dumps(final_report, indent=2, ensure_ascii=False))
    return final_report


def main():
    generate_report()

if __name__ == "__main__":
    main()
