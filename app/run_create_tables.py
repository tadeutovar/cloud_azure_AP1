from app.database.mysql import Base, engine
from app.models.card import Card
from app.models.user import User


Base.metadata.create_all(bind=engine)