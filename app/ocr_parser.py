import pytesseract
from PIL import Image
import re
from datetime import datetime

# Update this path if Tesseract is installed elsewhere on your system
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text(file):
    if file.type in ["image/png", "image/jpeg", "image/jpg"]:
        img = Image.open(file)
        return pytesseract.image_to_string(img)
    elif file.type == "text/plain":
        return file.read().decode("utf-8")
    return ""

def parse_receipt(text):
    vendor_match = re.search(r"(?i)vendor[:\-]?\s*(.+)", text)
    date_match = re.search(r"\d{2}/\d{2}/\d{4}", text)
    amount_match = re.search(r"\d+\.\d{2}", text)

    raw_vendor = vendor_match.group(1).strip() if vendor_match else "Unknown"
    # Clean vendor text by removing URLs and special characters
    vendor = re.sub(r"(\.com|\.in|\.net|https?://|www\.|/|\\|;|'|\")", "", raw_vendor)
    vendor = re.sub(r"[^\w\s]", "", vendor)
    vendor = re.sub(r"\s+", " ", vendor).strip()

    date_str = date_match.group(0) if date_match else datetime.today().strftime("%d/%m/%Y")

    try:
        parsed_date = datetime.strptime(date_str, "%d/%m/%Y")
        if parsed_date.year > 2100:
            date_str = datetime.today().strftime("%d/%m/%Y")
    except Exception:
        date_str = datetime.today().strftime("%d/%m/%Y")

    amount = float(amount_match.group(0)) if amount_match else 0.0

    return {
        "vendor": vendor,
        "date": date_str,
        "amount": amount,
        "category": "General"
    }
