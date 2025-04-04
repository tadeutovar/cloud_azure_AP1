from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Substitua pelas suas credenciais locais
MYSQL_USER = "root"
MYSQL_PASSWORD = "admin"
MYSQL_HOST = "localhost"
MYSQL_PORT = "3306"
MYSQL_DB = "api_ecommerce"

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()