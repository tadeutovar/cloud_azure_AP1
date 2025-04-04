# app/database.py
from pymongo import MongoClient

# Conectar com o MongoDB
client = MongoClient("mongodb://localhost:27017")  # Conexão local, altere conforme necessário
