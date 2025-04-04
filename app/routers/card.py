from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.mysql import get_db
from app.models.card import Card as CardModel
from app.models.user import User as UserModel
from app.schemas.card import CardCreate, CardOut

router = APIRouter()

# Criar cartão para um usuário
@router.post("/users/{user_id}/cards/", response_model=CardOut)
def create_card(user_id: int, card: CardCreate, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_card = CardModel(**card.dict(), user_id=user_id)
    db.add(new_card)
    db.commit()
    db.refresh(new_card)
    return new_card

# Listar cartões de um usuário
@router.get("/users/{user_id}/cards/", response_model=list[CardOut])
def get_user_cards(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return db.query(CardModel).filter(CardModel.user_id == user_id).all()

# Atualizar cartão
@router.put("/users/{user_id}/cards/{card_id}")
def update_card(user_id: int, card_id: int, card_data: dict, db: Session = Depends(get_db)):
    card = db.query(CardModel).filter(CardModel.id == card_id, CardModel.user_id == user_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    for key, value in card_data.items():
        setattr(card, key, value)
    db.commit()
    return {"message": "Card updated successfully"}

# Deletar cartão
@router.delete("/users/{user_id}/cards/{card_id}")
def delete_card(user_id: int, card_id: int, db: Session = Depends(get_db)):
    card = db.query(CardModel).filter(CardModel.id == card_id, CardModel.user_id == user_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    db.delete(card)
    db.commit()
    return {"message": "Card deleted successfully"}
