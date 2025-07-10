from fastapi import FastAPI
import datetime
import bcrypt

app = FastAPI()

productID_ =2

JWT_SECRET = "JWT"

inventario = [
    {
        "productID": 1,
        "name": "Manzana",
        "currentStock": 2,
        "minimunStock": 1,
        "lastUpdated": datetime.datetime.utcnow()
    },
    {
        "productID": 2,
        "name": "Mango",
        "currentStock": 5,
        "minimunStock": 2,
        "lastUpdated": datetime.datetime.utcnow()
    }
]

users = [
    {
        "id": 1,
        "name": "Iván",
        "email": "ivan@gmail.com",
        "password": bcrypt.hashpw("prueba123".encode('utf-8'), bcrypt.gensalt())
    }
]

@app.get("/")
def getInventory():
    return 1