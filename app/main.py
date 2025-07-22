import streamlit as st
import pandas as pd
from ocr_parser import extract_text, parse_receipt
from database import save_receipt, get_all_receipts
from search_sort import (
    search_vendor,
    sort_receipts,
    filter_by_amount_range,
    filter_by_date_range
)
from aggregator import get_aggregates

# Smart Category Detection Function
def auto_assign_category(vendor: str) -> str:
    vendor = vendor.lower()
    if "amazon" in vendor or "flipkart" in vendor:
        return "Shopping"
    elif "big bazaar" in vendor or "reliance" in vendor or "dmart" in vendor:
        return "Groceries"
    elif "restaurant" in vendor or "cafe" in vendor or "food" in vendor:
        return "Dining"
    elif "hospital" in vendor or "clinic" in vendor or "pharma" in vendor:
        return "Medical"
    elif "airtel" in vendor or "jio" in vendor or "vodafone" in vendor or "bill" in vendor:
        return "Utilities"
    elif "uber" in vendor or "ola" in vendor or "indigo" in vendor or "flight" in vendor:
        return "Travel"
    else:
        return "Other"

#Streamlit Setup
st.set_page_config(page_title="Receipt Desk", layout="wide")
st.title("Receipt Desk")

# Initialize session state for dataframe
if "df" not in st.session_state:
    st.session_state.df = get_all_receipts()

#Upload Section
st.header("Upload Receipt")
file = st.file_uploader("Upload a receipt (PNG, JPG, or TXT)", type=["png", "jpg", "jpeg", "txt"])

if file:
    extracted_text = extract_text(file)
    st.text_area("Extracted Text", extracted_text, height=200)

    if st.button("Parse and Edit Fields", key="parse_btn"):
        data = parse_receipt(extracted_text)
        st.session_state.parsed_data = data

#Parsed Data Correction Form
if "parsed_data" in st.session_state:
    st.subheader("Edit Parsed Data")
    data = st.session_state.parsed_data

    vendor = st.text_input("Vendor", value=data['vendor'], key="vendor_input")
    date = st.text_input("Date (dd/mm/yyyy)", value=data['date'], key="date_input")
    amount = st.number_input("Amount", value=float(data['amount']), step=1.0, format="%.2f", key="amount_input")

    # Smart Category Suggestion
    auto_category = auto_assign_category(vendor)

    categories = ["Groceries", "Utilities", "Electronics", "Dining", "Medical", "Travel", "Shopping", "Other"]
    selected = st.selectbox("Choose Category", categories, index=categories.index(auto_category) if auto_category in categories else len(categories)-1, key="category_select")

    if selected == "Other":
        category = st.text_input("Custom Category", value=auto_category, key="category_custom")
    else:
        category = selected

    if st.button("Save Corrected Receipt", key="save_btn"):
        corrected_data = {
            "vendor": vendor,
            "date": date,
            "amount": amount,
            "category": category
        }
        save_receipt(corrected_data)
        st.success(f"Saved:\nVendor: {vendor}\nDate: {date}\nAmount: ₹{amount:.2f}")

        # Refresh the session state data
        st.session_state.df = get_all_receipts()
        del st.session_state.parsed_data

#Receipt History Table
df = st.session_state.df
st.subheader("Receipt History")
st.dataframe(df)

#Smart Search
st.subheader("Smart Vendor Search")
search_input = st.text_input("Enter Vendor Name :", key="search_input")
if search_input:
    results = search_vendor(search_input)
    st.dataframe(results)

#Filter by Amount
st.subheader("Filter by Amount Range")
min_amount = st.number_input("Minimum Amount", value=0.0, step=1.0, format="%.2f", key="min_amount")
max_amount = st.number_input("Maximum Amount", value=10000.0, step=1.0, format="%.2f", key="max_amount")
if st.button("Apply Amount Filter", key="amount_filter_btn"):
    filtered_df = filter_by_amount_range(df, min_amount, max_amount)
    st.dataframe(filtered_df)

#Filter by Date
st.subheader("Filter by Date Range")
start_date = st.date_input("Start Date", key="start_date")
end_date = st.date_input("End Date", key="end_date")
if st.button("Apply Date Filter", key="date_filter_btn"):
    filtered_df = filter_by_date_range(df, start_date, end_date)
    st.dataframe(filtered_df)

#Sort Receipts
st.subheader("Sort Receipts")
sort_by = st.selectbox("Choose Field:", ["vendor", "date", "amount", "category"], key="sort_select")
if st.button("Sort Receipts", key="sort_btn"):
    sorted_df = sort_receipts(sort_by)
    st.dataframe(sorted_df)

# Summary Insights
st.subheader("Insights")
agg = get_aggregates()
if agg:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total", f"₹{agg['total']:.2f}")
    col2.metric("Average", f"₹{agg['mean']:.2f}")
    col3.metric("Most Frequent Amount", f"₹{agg['mode']:.2f}")
    st.line_chart(agg["monthly"].astype(float))

# Export CSV for download
if not df.empty:
    csv = df.to_csv(index=False)
    st.download_button(
        label="⬇ Download CSV",
        data=csv,
        file_name="receipts_export.csv",
        mime="text/csv",
        key="download_csv"
    )

# Export JSON for download
if not df.empty:
    json_data = df.to_json(orient="records", indent=2)
    st.download_button(
        label="⬇ Download JSON",
        data=json_data,
        file_name="receipts_export.json",
        mime="application/json",
        key="download_json"
    )