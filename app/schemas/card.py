# schemas/card.py

from pydantic import BaseModel, field_validator
from datetime import datetime

class CardCreate(BaseModel):
    number: str
    expiration_date: str  # formato MM/YY
    cvv: str
    balance: float

    @field_validator('expiration_date')
    def validate_expiration_date(cls, v):
        try:
            exp_date = datetime.strptime(v, "%m/%y")
            exp_date = datetime(exp_date.year, exp_date.month, 1)
            now = datetime.now()
            if exp_date < datetime(now.year, now.month, 1):
                raise ValueError("Card has expired")
        except ValueError:
            raise ValueError("Invalid expiration date format. Use MM/YY")
        return v


class CardOut(CardCreate):
    id: int
    user_id: int

    class Config:
        orm_mode = True
