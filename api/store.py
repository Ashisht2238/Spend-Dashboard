from functools import lru_cache
from pathlib import Path

from src.anomaly import flag_anomalies
from src.data import load_data

# Folder of this file is api/, so its parent is the project root.
CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "purchase_orders.csv"


@lru_cache(maxsize=1)
def get_df():
    """Load the CSV and flag unusual orders. Runs once; later calls reuse the result."""
    df = load_data(CSV_PATH)
    df = flag_anomalies(df, contamination=0.015)
    return df