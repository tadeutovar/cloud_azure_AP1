# app/models/user.py

from pydantic import BaseModel
from typing import List

class User(BaseModel):
    name: str
    email: str
    cards: List[str] = []  # Lista de IDs de cartões associados ao usuário
