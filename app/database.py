import sqlite3
import pandas as pd

conn = sqlite3.connect("receipts.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS receipts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vendor TEXT,
    date TEXT,
    amount REAL,
    category TEXT
)
""")
conn.commit()

def save_receipt(data):
    cursor.execute(
        "INSERT INTO receipts (vendor, date, amount, category) VALUES (?, ?, ?, ?)",
        (data["vendor"], data["date"], data["amount"], data["category"])
    )
    conn.commit()

def get_all_receipts():
    return pd.read_sql_query("SELECT * FROM receipts", conn)
