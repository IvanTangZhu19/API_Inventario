from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
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
        "lastUpdated": datetime.datetime.utcnow().isoformat()
    },
    {
        "productID": 2,
        "name": "Mango",
        "currentStock": 5,
        "minimunStock": 2,
        "lastUpdated": datetime.datetime.utcnow().isoformat()
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

@app.get("/inventory", status_code=200)
def getProducts():
    return inventario

@app.get("/inventory/{productID}")
def getProductByID(productID: int):
    if (productID is not None):
        for i in inventario:
            if i["productID"] == productID :
                return JSONResponse(content=i, status_code=200)
        return JSONResponse(
            content=
                {"error": {
                    "code": "ABC",
                    "message": "ProductoId no encontrado",
                    "details": "Parámetro productId no encontrado en la base de datos"
                }},
            status_code=404
        )
    else:
        return JSONResponse(
            content=
                {"error": {
                    "code": "ABC",
                    "message": "Parámetros incorrectos",
                    "details": "productId incorrecto"
                }},
            status_code=400
        )
    
@app.post("/inventory")
async def addProducts(request: Request):
    global productID_
    data = await request.json()
    name = data["name"]
    minimunStock = data["minimunStock"]
    quantity = data["quantity"] 
    if (name is None or minimunStock is None or quantity is None) :
        return JSONResponse(
            content=
                {"error": {
                    "code": "ABC",
                    "message": "Falta información",
                    "details": "Falta información (name, minimunStock, quantity)"
                }},
            status_code=400
        )
    if (minimunStock < 0 or quantity < 0) :
        return JSONResponse(
            content=
                {"error": {
                    "code": "ABC",
                    "message": "Cantidades deben ser mayores a cero",
                    "details": "Cantidades: minimunStock, quantity deben ser mayores a cero"
                }},
            status_code=400
        )
    productID_ = productID_ + 1
    inventario.append({
        "productID": productID_,
        "name": name,
        "quantity": quantity,
        "minimunStock": minimunStock,
        "lastUpdated": datetime.datetime.utcnow()
    })
    return JSONResponse(
        content=
            {"success": {
                "code": "ABC",
                "message": "Se añadió correctamente"
            }},
        status_code=201
    )