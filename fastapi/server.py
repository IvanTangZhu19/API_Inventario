from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import datetime
import bcrypt
import jwt

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
    name = data.get("name")
    minimunStock = data.get("minimunStock")
    quantity = data.get("quantity") 
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
        "currentStock": quantity,
        "minimunStock": minimunStock,
        "lastUpdated": datetime.datetime.utcnow().isoformat()
    })
    return JSONResponse(
        content=
            {"success": {
                "code": "ABC",
                "message": "Se añadió correctamente"
            }},
        status_code=201
    )

@app.put("/inventory/{productID}")
async def updateProduct(productID: int, request: Request):
    data = await request.json()
    name = data.get("name")
    quantity = data.get("quantity") 
    operation = data.get("operation") 
    if (name is None or quantity is None or operation is None) :
        return JSONResponse(
            content=
                {"error": {
                    "code": "ABC",
                    "message": "Falta información",
                    "details": "Falta información (name, minimunStock, quantity)"
                }},
            status_code=400
        )
    if quantity <= 0 :
        return JSONResponse(
            content=
                {"error": {
                    "code": "ABC",
                    "message": "Información incorrecta",
                    "details": "Quantity debe ser mayor a cero"
                }},
            status_code=400
        )
    if(operation != "add" and operation != "substract"):
        return JSONResponse(
            content=
                {"error": {
                    "code": "ABC",
                    "message": "Información incorrecta",
                    "details": "Operation tiene que ser add o substract"
                }},
            status_code=400
        )
    for i in inventario:
        if (i["productID"] == productID) :
            if (operation == "substract" and i["currentStock"] >= quantity):
                i["currentStock"] -= quantity
            elif (operation == "substract" and i["currentStock"] < quantity):
                return JSONResponse(
                    content=
                        {"error": {
                            "code": "ABC",
                            "message": "Cantidad erronea",
                            "details": "No hay suficientes existencias del producto"
                        }},
                    status_code=400
                )
            elif (operation == "add"):
                i["currentStock"] += quantity
            i["name"] = name
            i["lastUpdated"] = datetime.datetime.utcnow().isoformat()
            return JSONResponse(
                content=
                    {"success": {
                        "code": "ABC",
                        "message": "Se actualizó correctamente"
                    }},
                status_code=200
            )
        else:
            return JSONResponse(
                content=
                    {"error": {
                        "code": "ABC",
                        "message": "ProductoId no encontrado",
                        "details": "Parámetro productId no encontrado en la base de datos"
                    }},
                status_code=404
            )

@app.delete("/inventory/{productID}")
def deleteProductByID(productID: int):
    if (productID is not None):
        for i in inventario:
            if i["productID"] == productID :
                inventario.remove(i)
                return JSONResponse(
                    content=
                        {"success": {
                            "code": "ABC",
                            "message": "Se eliminó correctamente"
                        }},
                    status_code=200
                )
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
            status_code=404
        )

@app.get("/users/login")
async def login(request: Request):
    data = await request.json()
    email = data.get("email")
    password = data.get("password") 
    if email is None or password is None :
       return JSONResponse(
            content=
                {"error": {
                    "code": "ABC",
                    "message": "Falta información",
                    "details": "Falta información (name, minimunStock, quantity)"
                }},
            status_code=400
        )
    user = next((u for u in users if u["email"] == email), None)
    if(user is None):
        return JSONResponse(
            content=
                {"error": {
                    "code": "ABC",
                    "message": "Usuario no existe",
                    "details": "Usuario no encontrado en base de datos"
                }},
            status_code=400
        )
    if bcrypt.checkpw(password.encode('utf-8'), user["password"]):
        pass
    else:
        return JSONResponse(
            content=
                {"error": {
                    "code": "ABC",
                    "message": "Contraseña incorrecta",
                    "details": "Contraseña incorrecta"
                }},
            status_code=400
        )
    token = jwt.encode({
        "id": user["id"],
        "name": user["name"],
        "exp": datetime.datetime.utcnow()+ datetime.timedelta(hours=1)
    }, JWT_SECRET, algorithm="HS256")
    return JSONResponse(
        content=
            {"success": {
            "code": "ABC",
            "message": "Login correcto",
            "token": token
        }},
        status_code=200
    )