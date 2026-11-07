COLUMNS = [
    "po_number",
    "po_date",
    "vendor",
    "category",
    "item",
    "quantity",
    "unit_price",
    "total_amount",
]


def flagged_orders(df):
    """The orders flagged as unusual, biggest first, as a list of dictionaries."""
    flagged = df[df["is_anomaly"]].sort_values("total_amount", ascending=False)
    table = flagged[COLUMNS].copy()
    table["po_date"] = table["po_date"].dt.strftime("%Y-%m-%d")
    return table.to_dict(orient="records")