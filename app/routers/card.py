# app/routers/card.py

from fastapi import APIRouter
from app.database import client
from app.models.card import Card
from bson import ObjectId

router = APIRouter()

@router.post("/users/{user_id}/cards/")
async def create_card(user_id: str, card: dict):
    users_collection = client.db.users
    cards_collection = client.db.cards

    # Verifica se o usuário existe
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Insere o novo cartão
    card["user_id"] = user_id
    card_id = cards_collection.insert_one(card).inserted_id

    # Adiciona o cartão na lista de cartões do usuário
    users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$push": {"cards": str(card_id)}}
    )

    return {"message": "Card created successfully", "card_id": str(card_id)}

def serialize_card(card):
    card["_id"] = str(card["_id"])
    return card

@router.get("/users/{user_id}/cards/")
async def get_user_cards(user_id: str):
    users_collection = client.db.users
    cards_collection = client.db.cards

    # Verifica se o usuário existe
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        return {"error": "User not found"}

    # Converte os card_ids para string antes de buscar no banco
    card_ids = [ObjectId(card_id) for card_id in user.get("cards", []) if ObjectId.is_valid(card_id)]
    cards = list(cards_collection.find({"_id": {"$in": card_ids}}))

    # Converte os cartões para formato JSON-friendly
    return [serialize_card(card) for card in cards]
