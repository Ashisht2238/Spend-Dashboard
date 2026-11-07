from datetime import date

import pandas as pd

from api.store import get_df


def get_filtered_df(
    vendor: str | None = None,
    category: str | None = None,
    department: str | None = None,
    status: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
):
    """Return only the rows that match the filters the caller supplied."""
    df = get_df()
    if vendor:
        df = df[df["vendor"] == vendor]
    if category:
        df = df[df["category"] == category]
    if department:
        df = df[df["department"] == department]
    if status:
        df = df[df["status"] == status]
    if start_date:
        df = df[df["po_date"] >= pd.Timestamp(start_date)]
    if end_date:
        df = df[df["po_date"] <= pd.Timestamp(end_date)]
    return df