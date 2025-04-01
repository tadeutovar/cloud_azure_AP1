from fastapi import APIRouter, HTTPException
from app.database import client
from app.models.order import Order
from bson import ObjectId
from fastapi.encoders import jsonable_encoder

router = APIRouter()

users_collection = client.db.users
cards_collection = client.db.cards
products_collection = client.db.products
orders_collection = client.db.orders

@router.post("/orders/")
async def create_order(order: Order):
    # Verifica se o usuário existe pelo e-mail
    user = users_collection.find_one({"email": order.user_email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Verifica se o cartão pertence ao usuário e se os dados estão corretos
    card = cards_collection.find_one({
        "user_id": str(user["_id"]),  # Converte para string
        "number": order.card_number,
        "cvv": order.cvv
    })

    if not card:
        raise HTTPException(status_code=404, detail="Invalid card or card does not belong to user")

    # Calcula o total do pedido
    total_price = 0
    for item in order.products:
        product = products_collection.find_one({"_id": ObjectId(item.product_id)})
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        total_price += product["price"] * item.quantity

    # Verifica saldo do cartão
    if card["balance"] < total_price:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    # Debita o valor do cartão
    cards_collection.update_one(
        {"_id": card["_id"]},
        {"$set": {"balance": card["balance"] - total_price}}
    )

    # Salva o pedido
    order_dict = order.dict()
    order_dict["user_id"] = user["_id"]
    order_dict["total_price"] = total_price
    order_dict["status"] = "confirmed"

    result = orders_collection.insert_one(order_dict)
    return {"id": str(result.inserted_id), "total_price": total_price, "status": "confirmed"}

def serialize_order(order):
    # Convertendo ObjectId para string antes de retornar o pedido
    order = dict(order)  # Convertendo o MongoDB document para dict
    for key, value in order.items():
        if isinstance(value, ObjectId):
            order[key] = str(value)  # Convertendo ObjectId para string
    return order

# Listar todos os pedidos
@router.get("/orders/")
async def get_all_orders():
    orders = list(orders_collection.find())
    
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found")

    # Serializando os pedidos antes de retornar
    return [serialize_order(order) for order in orders]

# Listar pedidos por ID do usuário
@router.get("/orders/{user_id}")
async def get_orders_by_user(user_id: str):
    # Verifica se o user_id é um ObjectId válido
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user_id format")
    
    # Busca os pedidos do usuário
    orders = list(orders_collection.find({"user_id": ObjectId(user_id)}))  # Convertendo user_id para ObjectId

    if not orders:
        raise HTTPException(status_code=404, detail="No orders found for this user")

    # Serializando os pedidos antes de retornar
    return [serialize_order(order) for order in orders]
