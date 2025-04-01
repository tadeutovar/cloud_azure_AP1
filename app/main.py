from fastapi import FastAPI
from app.routers import user, card, product, order

app = FastAPI()

# Incluindo os routers
app.include_router(user.router)
app.include_router(card.router)
app.include_router(product.router)
app.include_router(order.router)

@app.get("/")
def home():
    return {"message": "API is running"}
