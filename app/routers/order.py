from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from datetime import datetime

# Banco de dados
from app.database.mysql import get_db
from app.database.database_mongo import client

# Models do MySQL
from app.models.user import User
from app.models.card import Card

# Schema do pedido (Pydantic)
from app.models.order import Order

router = APIRouter()

# Coleções MongoDB
products_collection = client.db.products
orders_collection = client.db.orders

# Serializador para retornar ObjectId como string
def serialize_order(order):
    order = dict(order)
    for key, value in order.items():
        if isinstance(value, ObjectId):
            order[key] = str(value)
    return order

# Criar pedido
@router.post("/orders/")
async def create_order(order: Order, db: Session = Depends(get_db)):
    # Verifica se o usuário existe no MySQL
    user = db.query(User).filter(User.email == order.user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Verifica se o cartão pertence ao usuário e dados estão corretos
    card = db.query(Card).filter(
        Card.user_id == user.id,
        Card.number == order.card_number,
        Card.cvv == order.cvv
    ).first()

    if not card:
        raise HTTPException(status_code=404, detail="Invalid card or card does not belong to user")

    # Calcula total do pedido
    total_price = 0
    for item in order.products:
        product = products_collection.find_one({"_id": ObjectId(item.product_id)})
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        total_price += product["price"] * item.quantity

    # Verifica saldo
    if card.balance < total_price:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    # Debita o valor do cartão
    card.balance -= total_price
    db.commit()

    # Salva o pedido no MongoDB
    order_dict = order.dict()
    order_dict["user_id"] = user.id  # agora é int, não ObjectId
    order_dict["total_price"] = total_price
    order_dict["status"] = "confirmed"
    order_dict["created_at"] = datetime.utcnow()

    result = orders_collection.insert_one(order_dict)

    return {
        "id": str(result.inserted_id),
        "total_price": total_price,
        "status": "confirmed"
    }

# Listar todos os pedidos
@router.get("/orders/")
async def get_all_orders():
    orders = list(orders_collection.find())
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found")
    return [serialize_order(order) for order in orders]

# Listar pedidos por ID do usuário (MySQL)
@router.get("/orders/{user_id}")
async def get_orders_by_user(user_id: int):
    orders = list(orders_collection.find({"user_id": user_id}))
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found for this user")
    return [serialize_order(order) for order in orders]
