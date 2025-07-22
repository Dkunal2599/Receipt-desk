from pydantic import BaseModel

class Receipt(BaseModel):
    vendor: str
    date: str
    amount: float
    category: str
