# app/main.py

from fastapi import FastAPI
from app.routers import user, card

app = FastAPI()

# Incluir as rotas de usuário e cartão
app.include_router(user.router)
app.include_router(card.router)
