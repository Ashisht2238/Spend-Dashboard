def spend_by(df, column):
    """Total spend for each value of one column (vendor or category), biggest first."""
    grouped = (
        df.groupby(column)["total_amount"]
        .sum()
        .sort_values(ascending=False)
    )
    return [
        {column: name, "total_spend": round(float(value), 2)}
        for name, value in grouped.items()
    ]


def monthly_spend(df):
    """Total spend for each month, oldest first."""
    grouped = df.groupby("month")["total_amount"].sum().sort_index()
    return [
        {"month": month.strftime("%Y-%m"), "total_spend": round(float(value), 2)}
        for month, value in grouped.items()
    ]