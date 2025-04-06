from fastapi import APIRouter, HTTPException
from app.database.database_mongo import client
from app.models.product import Product
from bson import ObjectId

router = APIRouter()

# Coleção de produtos no MongoDB
products_collection = client.db.products

def serialize_product(product):
    """ Converte o _id do MongoDB para string """
    product["_id"] = str(product["_id"])
    return product

# Criar um produto
@router.post("/products/")
async def create_product(product: Product):
    product_dict = product.dict()
    result = products_collection.insert_one(product_dict)
    return {"id": str(result.inserted_id)}

# Listar todos os produtos
@router.get("/products/")
async def get_all_products():
    products = list(products_collection.find())
    return [serialize_product(product) for product in products]

# Buscar produto por ID
@router.get("/products/{product_id}")
async def get_product_by_id(product_id: str):
    product = products_collection.find_one({"_id": ObjectId(product_id)})
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return serialize_product(product)

# Atualizar produto
@router.put("/products/{product_id}")
async def update_product(product_id: str, product_data: dict):
    if not products_collection.find_one({"_id": ObjectId(product_id)}):
        raise HTTPException(status_code=404, detail="Product not found")

    products_collection.update_one({"_id": ObjectId(product_id)}, {"$set": product_data})
    return {"message": "Product updated successfully"}

# Deletar produto
@router.delete("/products/{product_id}")
async def delete_product(product_id: str):
    result = products_collection.delete_one({"_id": ObjectId(product_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"message": "Product deleted successfully"}
