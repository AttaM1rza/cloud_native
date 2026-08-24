from datetime import date

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Receipt API")


class ReceiptItem(BaseModel):
    name: str
    quantity: int
    price: float


class Receipt(BaseModel):
    id: int
    merchant: str
    date: date
    total: float
    currency: str = "EUR"
    items: list[ReceiptItem] = []


# TODO dummy daten

receipts: list[Receipt] = [
    Receipt(
        id=1,
        merchant="Supermarkt Müller",
        date=date(2026, 8, 20),
        total=12.47,
        items=[
            ReceiptItem(name="Milch", quantity=2, price=1.29),
            ReceiptItem(name="Brot", quantity=1, price=9.89),
        ],
    ),
    Receipt(
        id=2,
        merchant="Baumarkt Nord",
        date=date(2026, 8, 22),
        total=34.90,
        items=[ReceiptItem(name="Schrauben", quantity=1, price=34.90)],
    ),
]


@app.get("/")
def read_root():
    return {"message": "Receipt Service"}


@app.get("/receipts")
def list_receipts() -> list[Receipt]:
    return receipts


@app.post("/receipts", status_code=201)
def create_receipt(receipt: Receipt) -> Receipt:
    if any(existing.id == receipt.id for existing in receipts):
        raise HTTPException(status_code=409, detail="Receipt id already exists")
    receipts.append(receipt)
    return receipt
