# 🧾 Receipt Desk
A smart, searchable, OCR-powered receipt management system built with Python & Streamlit.

## ✨ Features

- Upload receipts in image or text format
- Extract and parse text using OCR (Tesseract)
- Auto-detect vendor, date, amount, and category
- Smart category suggestions (based on vendor)
- Search and filter receipts by vendor, amount, and date
- View and sort receipt history
- Export data as CSV or JSON
- Dashboard insights: total, average, frequent amount, monthly trend

## 🛠️ Tech Stack

- Python 3
- Streamlit
- Pandas
- SQLite
- Pytesseract (OCR)
- PIL (Image processing)

## 🚀 Getting Started

1. Clone the repo:
```bash
git clone https://github.com/your-username/receipt-desk.git
cd receipt-desk
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Make sure Tesseract OCR is installed:
[Install Tesseract](https://github.com/tesseract-ocr/tesseract)

4. Run the app:
```bash
streamlit run main.py
```

## 📂 Project Structure

```
receipt-desk/
├── main.py
├── ocr_parser.py
├── database.py
├── search_sort.py
├── aggregator.py
├── model.py
├── receipts.db
├── data/
│   └── receipts_export.csv
├── requirements.txt
└── README.md
```

## 🛠️ Future Improvements

- Add login/user support
- Save to cloud storage
- Train ML model for smarter category prediction
- Export to Excel & PDF
- Mobile responsive design
