from pydantic import BaseModel
from typing import List

class Product(BaseModel):
    productCategory: str
    productName: str
    price: float
    imageUrl: List[str]
    productDescription: str
