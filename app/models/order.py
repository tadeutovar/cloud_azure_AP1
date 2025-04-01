from pydantic import BaseModel
from typing import List

class OrderItem(BaseModel):
    product_id: str
    quantity: int

class Order(BaseModel):
    user_email: str
    card_number: str
    cvv: str
    products: List[OrderItem]
