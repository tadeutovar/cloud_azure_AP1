from pydantic import BaseModel

class CardCreate(BaseModel):
    number: str
    expiration_date: str
    cvv: str
    balance: float

class CardOut(CardCreate):
    id: int
    user_id: int

    class Config:
        orm_mode = True
