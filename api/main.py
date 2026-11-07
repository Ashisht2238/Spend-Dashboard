from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.filtering import get_filtered_df
from api.forecasting import forecast_by_category
from api.orders import flagged_orders
from api.spending import monthly_spend, spend_by
from api.store import get_df

app = FastAPI(title="Spend Analytics API")

# Allow the React dev server (a different address) to read our data.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Load the data now, at startup, so a problem shows up immediately
# and the first request isn't slow.
get_df()


def options(column):
    """Sorted list of the distinct values in one column."""
    return sorted(get_df()[column].unique().tolist())


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/filters")
def filters():
    df = get_df()
    return {
        "vendors": options("vendor"),
        "categories": options("category"),
        "departments": options("department"),
        "statuses": options("status"),
        "min_date": df["po_date"].min().date().isoformat(),
        "max_date": df["po_date"].max().date().isoformat(),
    }


@app.get("/api/summary")                       # NEW endpoint
def summary(df=Depends(get_filtered_df)):
    return {
        "total_spend": round(float(df["total_amount"].sum()), 2),
        "total_orders": int(len(df)),
        "total_vendors": int(df["vendor"].nunique()),
        "flagged_orders": int(df["is_anomaly"].sum()),
    }


@app.get("/api/spend/vendor")
def spend_by_vendor(df=Depends(get_filtered_df)):
    return spend_by(df, "vendor")


@app.get("/api/spend/category")
def spend_by_category(df=Depends(get_filtered_df)):
    return spend_by(df, "category")


@app.get("/api/spend/monthly")
def spend_by_month(df=Depends(get_filtered_df)):
    return monthly_spend(df)

@app.get("/api/anomalies")
def anomalies(df=Depends(get_filtered_df)):
    orders = flagged_orders(df)
    return {"count": len(orders), "orders": orders}

@app.get("/api/forecast")
def forecast(df=Depends(get_filtered_df)):
    return forecast_by_category(df)