from src.forecast import forecast_next_month

MIN_FORECAST_MONTHS = 3


def forecast_by_category(df):
    """Predict next month's spend per category from the (filtered) normal orders."""
    # Leave out flagged orders so one huge order doesn't distort the trend
    normal_orders = df[~df["is_anomaly"]]

    if normal_orders["month"].nunique() < MIN_FORECAST_MONTHS:
        return {
            "next_month": None,
            "forecast": [],
            "message": f"Need at least {MIN_FORECAST_MONTHS} months of data to forecast.",
        }

    forecast, next_month = forecast_next_month(normal_orders)
    forecast = forecast.sort_values(ascending=False).round(0)

    return {
        "next_month": next_month.strftime("%Y-%m"),
        "forecast": [
            {"category": name, "forecast_spend": float(value)}
            for name, value in forecast.items()
        ],
        "message": None,
    }