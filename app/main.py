from fastapi import FastAPI
from app.routers import user, card, product

app = FastAPI()

# Incluindo os routers
app.include_router(user.router)
app.include_router(card.router)
app.include_router(product.router)  # <- Certifique-se de que esse está aqui!

@app.get("/")
def home():
    return {"message": "API is running"}
