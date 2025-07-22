import pandas as pd
import re
from database import get_all_receipts

def search_vendor(keyword):
    # Clean the keyword like we clean the vendor strings
    keyword = re.sub(r"(\.com|\.in|\.net|https?://|www\.|/|\\|;|'|\")", "", keyword)
    keyword = re.sub(r"[^\w\s]", "", keyword)
    keyword = re.sub(r"\s+", " ", keyword).strip()
    clean_keyword = keyword.lower().replace(" ", "")

    df = get_all_receipts()
    df["vendor_clean"] = df["vendor"].str.lower().str.replace(r"[^\w\s]", "", regex=True).str.replace(r"\s+", "", regex=True)
    return df[df["vendor_clean"].str.contains(clean_keyword, na=False)].drop(columns=["vendor_clean"])

def sort_receipts(col):
    df = get_all_receipts()
    if col in df.columns:
        return df.sort_values(by=col)
    else:
        return df

def filter_by_amount_range(df, min_amt, max_amt):
    # Returns receipts where amount is within [min_amt, max_amt]
    return df[(df['amount'] >= min_amt) & (df['amount'] <= max_amt)]

def filter_by_date_range(df, start_date, end_date):
    # Convert string dates to datetime and apply filter
    df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y", errors="coerce")
    return df[(df["date"] >= pd.to_datetime(start_date)) & (df["date"] <= pd.to_datetime(end_date))]
