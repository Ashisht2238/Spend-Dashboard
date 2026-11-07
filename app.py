import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from src.data import load_data
from src.anomaly import flag_anomalies
from src.forecast import forecast_next_month


# ---------- PAGE CONFIGURATION ----------
st.set_page_config(
    page_title="Spend Analytics Dashboard",
    layout="wide"
)

st.title("Spend Analytics Dashboard")
st.subheader("Purchase order spend, unusual orders and forecast")


# ---------- LOAD DATA ----------
@st.cache_data
def get_data():
    return load_data()


df = get_data()

# Convert date column
df["po_date"] = pd.to_datetime(df["po_date"])

# Extract month
df["month"] = df["po_date"].dt.to_period("M")

# Anomaly detection
df = flag_anomalies(df, contamination=0.015)


# ---------- FORMAT CURRENCY ----------
def format_lakhs(x, pos):
    return f"₹{x / 100000:.1f}L"


# ---------- HEADLINE NUMBERS ----------
c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Total Spend",
    f"₹ {df['total_amount'].sum():,.0f}"
)

c2.metric("Total Orders", f"{len(df):,}")

c3.metric("Total Vendors", df["vendor"].nunique())

c4.metric("Flagged Orders", int(df["is_anomaly"].sum()))



# ---------- SPEND ANALYSIS ----------
st.header("1. Spend Analysis")

# Calculate spending
vendor_spend = (
    df.groupby("vendor")["total_amount"]
    .sum()
    .sort_values(ascending=True)
)

category_spend = (
    df.groupby("category")["total_amount"]
    .sum()
    .sort_values(ascending=False)
)

monthly_spend = (
    df.groupby("month")["total_amount"]
    .sum()
    .sort_index()
)


# ---------- FIRST ROW ----------
left, right = st.columns(2)

# 1. Vendor-wise Spending
with left:

    st.subheader("Vendor-wise Spending")

    fig, ax = plt.subplots(figsize=(7, 5))

    ax.barh(
        vendor_spend.index,
        vendor_spend.values,
        color="purple"
    )

    ax.set_xlabel("Total Spending")
    ax.xaxis.set_major_formatter(FuncFormatter(format_lakhs))
    ax.grid(axis="x", linestyle="--", alpha=0.3)

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


# 2. Category-wise Spending
with right:

    st.subheader("Category-wise Spending")

    fig, ax = plt.subplots(figsize=(7, 5))

    ax.bar(
        category_spend.index,
        category_spend.values,
        color="skyblue"
    )

    ax.set_ylabel("Total Spending")
    ax.yaxis.set_major_formatter(FuncFormatter(format_lakhs))
    ax.tick_params(axis="x", rotation=30)
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


# ---------- SECOND ROW ----------
left, right = st.columns(2)

# 3. Monthly Spending Trend
with left:

    st.subheader("Monthly Spending Trend")

    fig, ax = plt.subplots(figsize=(7, 5))

    ax.plot(
        monthly_spend.index.astype(str),
        monthly_spend.values,
        color="green",
        marker="o",
        linewidth=2
    )

    ax.set_xlabel("Month")
    ax.set_ylabel("Total Spending")
    ax.yaxis.set_major_formatter(FuncFormatter(format_lakhs))
    ax.grid(True, linestyle="--", alpha=0.3)

    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)


# 4. Category Spending Distribution
with right:

    st.subheader("Category Spending Distribution")

    fig, ax = plt.subplots(figsize=(3, 2))

    ax.pie(
        category_spend.values,
        labels=category_spend.index,
        autopct="%1.1f%%",
        startangle=90
    )

    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)



# ---------- ANOMALY DETECTION ----------
st.header("2. Unusual Orders")

flagged = (
    df[df["is_anomaly"]]
    .sort_values("total_amount", ascending=False)
)

st.write(
    f"{len(flagged)} orders look unusual for their category."
)

if not flagged.empty:

    st.dataframe(
        flagged[
            [
                "po_number",
                "po_date",
                "vendor",
                "category",
                "item",
                "quantity",
                "unit_price",
                "total_amount"
            ]
        ],
        width="stretch"
    )

else:
    st.success("No unusual orders detected.")


# ---------- FORECAST ----------
st.header("3. Forecast: Next Month's Spend")

normal_orders = df[~df["is_anomaly"]]

MIN_FORECAST_MONTHS = 3

if normal_orders["month"].nunique() < MIN_FORECAST_MONTHS:

    st.warning("Need at least 3 months of data to forecast.")

else:

    forecast, next_month = forecast_next_month(normal_orders)

    forecast = forecast.sort_values(
        ascending=False
    ).round(0)

    st.write(
        f"Predicted spend for **{next_month:%B %Y}**"
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.bar(
        forecast.index,
        forecast.values,
        color="orange"
    )

    ax.set_xlabel("Category")
    ax.set_ylabel("Predicted Spending")
    ax.yaxis.set_major_formatter(FuncFormatter(format_lakhs))
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)











# import streamlit as st
# import plotly.express as px

# from src.data import load_data
# from src.anomaly import flag_anomalies
# from src.forecast import forecast_next_month


# # ---------- PAGE CONFIGURATION ----------
# st.set_page_config(
#     page_title="Spend Analytics",
#     layout="wide"
# )

# st.title("Spend Analytics Dashboard")
# st.write("Analyze purchase orders and company spending.")


# # ---------- LOAD DATA ----------
# @st.cache_data
# def get_data():
#     return load_data()


# df = get_data()
# df = flag_anomalies(df, contamination=0.015)


# # ---------- COMMON CHART SETTINGS ----------
# CHART_CONFIG = {
#     "staticPlot": True,
#     "displayModeBar": False
# }


# # ---------- HEADLINE NUMBERS ----------
# c1, c2, c3, c4 = st.columns(4)

# c1.metric("Total Spend",f"₹ {df['total_amount'].sum():,.0f}")
# c2.metric("Total Orders",f"{len(df):,}")
# c3.metric("Total Vendors",df["vendor"].nunique())
# c4.metric("Flagged Orders",int(df["is_anomaly"].sum()))

# # ---------- SPEND CHARTS ----------
# st.header("1. Spend Charts")
# left, right = st.columns(2)

# # ---------- BY VENDOR ----------
# with left:
#     st.subheader("Spend by Vendor")

#     vendor_data = (df.groupby("vendor", as_index=False)["total_amount"].sum().sort_values("total_amount", ascending=False))

#     fig_vendor = px.bar(vendor_data, x="vendor",y="total_amount",
#         labels={
#             "vendor": "Vendor",
#             "total_amount": "Total Spend (₹)"
#         }
#     )

#     fig_vendor.update_layout(
#         dragmode=False,
#         hovermode=False
#     )

#     st.plotly_chart(
#         fig_vendor,
#         use_container_width=True,
#         config=CHART_CONFIG
#     )


# # ---------- BY CATEGORY ----------
# with right:
#     st.subheader("Spend by Category")

#     category_data = (
#         df.groupby("category", as_index=False)["total_amount"]
#         .sum()
#         .sort_values("total_amount", ascending=False)
#     )

#     fig_category = px.bar(
#         category_data,
#         x="category",
#         y="total_amount",
#         labels={
#             "category": "Category",
#             "total_amount": "Total Spend (₹)"
#         },
#         title="Total Spend by Category"
#     )

#     fig_category.update_layout(
#         dragmode=False,
#         hovermode=False
#     )

#     st.plotly_chart(
#         fig_category,
#         use_container_width=True,
#         config=CHART_CONFIG
#     )


# # ---------- BY MONTH ----------
# st.subheader("Spend by Month")

# monthly_data = (
#     df.groupby("month", as_index=False)["total_amount"]
#     .sum()
#     .sort_values("month")
# )

# fig_month = px.bar(
#     monthly_data,
#     x="month",
#     y="total_amount",
#     labels={
#         "month": "Month",
#         "total_amount": "Total Spend (₹)"
#     },
#     title="Monthly Spending"
# )

# fig_month.update_layout(
#     dragmode=False,
#     hovermode=False
# )

# st.plotly_chart(
#     fig_month,
#     use_container_width=True,
#     config=CHART_CONFIG
# )


# # ---------- ANOMALY DETECTION ----------
# st.header("2. Unusual Orders")

# flagged = (
#     df[df["is_anomaly"]]
#     .sort_values("total_amount", ascending=False)
# )

# st.write(
#     f"{len(flagged)} orders look unusual for their category."
# )

# st.dataframe(
#     flagged[
#         [
#             "po_number",
#             "po_date",
#             "vendor",
#             "category",
#             "item",
#             "quantity",
#             "unit_price",
#             "total_amount"
#         ]
#     ],
#     use_container_width=True
# )


# # ---------- FORECAST ----------
# st.header("3. Forecast: Next Month's Spend")

# normal_orders = df[~df["is_anomaly"]]

# forecast, next_month = forecast_next_month(normal_orders)

# st.write(
#     f"Predicted spend for **{next_month:%B %Y}**"
# )

# forecast_data = (
#     forecast.rename("forecast_spend")
#     .rename_axis("category")
#     .reset_index()
# )

# fig_forecast = px.bar(
#     forecast_data,
#     x="category",
#     y="forecast_spend",
#     labels={
#         "category": "Category",
#         "forecast_spend": "Forecast Spend (₹)"
#     },
#     title="Predicted Spend by Category"
# )

# fig_forecast.update_layout(
#     dragmode=False,
#     hovermode=False
# )

# st.plotly_chart(
#     fig_forecast,
#     use_container_width=True,
#     config=CHART_CONFIG
# )

# st.caption(
#     "Forecasts use a simple linear trend and may not account "
#     "for seasonal spending changes."
# )


# # ---------- RAW DATA ----------
# with st.expander("Show Raw Data"):
#     st.dataframe(df, use_container_width=True)























# import numpy as np
# import pandas as pd
# import streamlit as st
# from sklearn.ensemble import IsolationForest

# st.set_page_config(page_title="Spend Analytics", layout="wide")
# st.title("Spend Analytics Dashboard")


# # ---------- 1. LOAD DATA ----------
# @st.cache_data
# def load_data():
#     df = pd.read_csv("data/purchase_orders.csv", parse_dates=["po_date"])
#     # Turn each date into the first day of its month, e.g. 2025-03-17 -> 2025-03-01
#     df["month"] = df["po_date"].dt.to_period("M").dt.to_timestamp()
#     return df


# # ---------- 2. ANOMALY DETECTION ----------
# def flag_anomalies(df, contamination):
#     """Mark unusual orders. Each category is checked separately,
#     because a normal laptop order looks very different from a normal pen order."""
#     df = df.copy()
#     df["is_anomaly"] = False
#     for category, group in df.groupby("category"):
#         # log1p squashes big numbers so the model compares sizes fairly
#         features = np.log1p(group[["quantity", "unit_price"]])
#         model = IsolationForest(contamination=contamination, random_state=42)
#         model.fit(features)
#         df.loc[group.index, "is_anomaly"] = model.predict(features) == -1
#     return df


# # ---------- 3. FORECAST ----------
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


# df = load_data()

# contamination = 0.015
# df = flag_anomalies(df, contamination)

# # # Sidebar control
# # st.sidebar.header("Settings")
# # contamination = st.sidebar.slider(
# #     "Share of orders to flag as unusual", 0.005, 0.05, 0.015, step=0.005,
# #     help="Higher = more orders get flagged",
# # )
# # df = flag_anomalies(df, contamination)

# # ---------- HEADLINE NUMBERS ----------
# c1, c2, c3, c4 = st.columns(4)
# c1.metric("Total spend", f"{df['total_amount'].sum():,.0f}")
# c2.metric("Orders", f"{len(df):,}")
# c3.metric("Vendors", df["vendor"].nunique())
# c4.metric("Flagged orders", int(df["is_anomaly"].sum()))

# # ---------- SPEND CHARTS ----------
# st.header("1. Spend breakdown")
# left, right = st.columns(2)
# with left:
#     st.subheader("By vendor")
#     st.bar_chart(df.groupby("vendor")["total_amount"].sum().sort_values(ascending=False))
# with right:
#     st.subheader("By category")
#     st.bar_chart(df.groupby("category")["total_amount"].sum().sort_values(ascending=False))

# st.subheader("By month")
# st.line_chart(df.groupby("month")["total_amount"].sum())

# # ---------- ANOMALIES ----------
# st.header("2. Unusual orders")
# flagged = df[df["is_anomaly"]].sort_values("total_amount", ascending=False)
# st.write(f"{len(flagged)} orders look unusual for their category.")
# st.dataframe(
#     flagged[["po_number", "po_date", "vendor", "category", "item",
#              "quantity", "unit_price", "total_amount"]],
#     width="stretch",
# )

# # ---------- FORECAST ----------
# st.header("3. Forecast: next month's spend by category")
# # Leave out flagged orders so one huge order doesn't distort the trend
# forecast, next_month = forecast_next_month(df[~df["is_anomaly"]])
# st.write(f"Predicted spend for **{next_month:%B %Y}**")
# st.bar_chart(forecast)
# st.dataframe(forecast.round(0).to_frame("forecast spend"))
# st.caption("Simple straight-line trend. It does not account for seasonal busy months.")

# with st.expander("Show raw data"):
#     st.dataframe(df)