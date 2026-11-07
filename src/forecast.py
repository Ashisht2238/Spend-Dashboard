# import numpy as np
# import pandas as pd


# def forecast_next_month(df):
#     """Draw a straight trend line through each category's monthly spend
#     and read off where it lands next month."""
#     monthly = df.pivot_table(
#         index="month", columns="category", values="total_amount", aggfunc="sum"
#     ).fillna(0)
#     x = np.arange(len(monthly))
#     results = {}
#     for category in monthly.columns:
#         slope, intercept = np.polyfit(x, monthly[category].values, 1)
#         results[category] = max(slope * len(monthly) + intercept, 0)
#     next_month = monthly.index[-1] + pd.offsets.MonthBegin(1)
#     return pd.Series(results, name="forecast"), next_month










import numpy as np
import pandas as pd


def forecast_next_month(df):

    # Step 1: Calculate monthly spending by category
    monthly = df.pivot_table(
        index="month",
        columns="category",
        values="total_amount",
        aggfunc="sum"
    ).fillna(0)

    # Step 2: Convert PeriodIndex to DatetimeIndex
    if isinstance(monthly.index, pd.PeriodIndex):
        monthly.index = monthly.index.to_timestamp()

    # Step 3: Create complete monthly date range
    all_months = pd.date_range(
        start=monthly.index.min(),
        end=monthly.index.max(),
        freq="MS"
    )

    # Step 4: Fill missing months with zero
    monthly = monthly.reindex(
        all_months,
        fill_value=0
    )

    # Step 5: Create numerical month positions
    x = np.arange(len(monthly))

    # Step 6: Predict next month's spending
    results = {}

    for category in monthly.columns:

        slope, intercept = np.polyfit(
            x,
            monthly[category].values,
            1
        )

        predicted_spend = slope * len(monthly) + intercept

        results[category] = max(predicted_spend, 0)

    # Step 7: Calculate next month
    next_month = (
        monthly.index[-1] + pd.offsets.MonthBegin(1)
    )

    # Step 8: Return forecast results
    return pd.Series(
        results,
        name="forecast"
    ), next_month
