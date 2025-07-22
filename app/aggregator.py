from database import get_all_receipts
import pandas as pd

def get_aggregates():
    df = get_all_receipts()
    if df.empty:
        return None

    # Convert string date to datetime
    df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y", errors="coerce")
    df.dropna(subset=["date"], inplace=True)

    # Group monthly by sum of amount
    monthly_trend = df.groupby(df["date"].dt.to_period("M"))["amount"].sum()
    monthly_trend.index = monthly_trend.index.to_timestamp()

    # Frequency distribution of vendors
    vendor_counts = df["vendor"].value_counts()

    return {
        "total": df["amount"].sum(),
        "mean": df["amount"].mean(),
        "median": df["amount"].median(),
        "mode": df["amount"].mode()[0] if not df["amount"].mode().empty else 0,
        "vendor_counts": vendor_counts,
        "monthly": monthly_trend
    }
