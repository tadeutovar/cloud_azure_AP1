# app/models/card.py

from pydantic import BaseModel

class Card(BaseModel):
    number: str
    expiration_date: str
    cvv: str
    balance: float
