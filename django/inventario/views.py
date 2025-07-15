from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import datetime
import json
import bcrypt
import jwt

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

@csrf_exempt
def Products(request):
    if request.method == "GET":
        return JsonResponse(inventario, safe=False)
    if request.method == "POST":
        global productID_
        data = json.loads(request.body)
        name = data.get("name")
        minimunStock = data.get("minimunStock")
        quantity = data.get("quantity") 
        if (name is None or minimunStock is None or quantity is None) :
            return JsonResponse({
                "error": {
                    "code": "ABC",
                    "message": "Falta información",
                    "details": "Falta información (name, minimunStock, quantity)"
                }
            }, status=400)
        if (minimunStock < 0 or quantity < 0) :
            return JsonResponse({
                "error": {
                    "code": "ABC",
                    "message": "Cantidades deben ser mayores a cero",
                    "details": "Cantidades: minimunStock, quantity deben ser mayores a cero"
                }
            }, status=400)
        productID_ = productID_ + 1
        inventario.append({
            "productID": productID_,
            "name": name,
            "currentStock": quantity,
            "minimunStock": minimunStock,
            "lastUpdated": datetime.datetime.utcnow().isoformat()
        })
        return JsonResponse({
            "success": {
                "code": "ABC",
                "message": "Se añadió correctamente",
            }
        }, status=201)

@csrf_exempt
def ProductByID(request, productID):
    if request.method == "GET":
        if (productID is not None):
            for i in inventario:
                if i["productID"] == productID :
                    return JsonResponse(i, status=200)
            return JsonResponse(
                    {"error": {
                        "code": "ABC",
                        "message": "ProductoId no encontrado",
                        "details": "Parámetro productId no encontrado en la base de datos"
                    }},
                status=404
            )
        else:
            return JsonResponse(
                    {"error": {
                        "code": "ABC",
                        "message": "Parámetros incorrectos",
                        "details": "productId incorrecto"
                    }},
                status=400
            )
    if request.method == "PUT":
        data = json.loads(request.body)
        name = data.get("name")
        quantity = data.get("quantity") 
        operation = data.get("operation") 
        if (name is None or quantity is None or operation is None) :
            return JsonResponse(
                    {"error": {
                        "code": "ABC",
                        "message": "Falta información",
                        "details": "Falta información (name, minimunStock, quantity)"
                    }},
                status=400
            )
        if quantity <= 0 :
            return JsonResponse(
                    {"error": {
                        "code": "ABC",
                        "message": "Información incorrecta",
                        "details": "Quantity debe ser mayor a cero"
                    }},
                status=400
            )
        if(operation != "add" and operation != "substract"):
            return JsonResponse(
                    {"error": {
                        "code": "ABC",
                        "message": "Información incorrecta",
                        "details": "Operation tiene que ser add o substract"
                    }},
                status=400
            )
        for i in inventario:
            if (i["productID"] == productID) :
                if (operation == "substract" and i["currentStock"] >= quantity):
                    i["currentStock"] -= quantity
                elif (operation == "substract" and i["currentStock"] < quantity):
                    return JsonResponse(
                            {"error": {
                                "code": "ABC",
                                "message": "Cantidad erronea",
                                "details": "No hay suficientes existencias del producto"
                            }},
                        status=400
                    )
                elif (operation == "add"):
                    i["currentStock"] += quantity
                i["name"] = name
                i["lastUpdated"] = datetime.datetime.utcnow().isoformat()
                return JsonResponse(
                        {"success": {
                            "code": "ABC",
                            "message": "Se actualizó correctamente"
                        }},
                    status=200
                )
            else:
                return JsonResponse(
                        {"error": {
                            "code": "ABC",
                            "message": "ProductoId no encontrado",
                            "details": "Parámetro productId no encontrado en la base de datos"
                        }},
                    status=404
                )
    if request.method == "DELETE":
        if (productID is not None):
            for i in inventario:
                if i["productID"] == productID :
                    inventario.remove(i)
                    return JsonResponse(
                            {"success": {
                                "code": "ABC",
                                "message": "Se eliminó correctamente"
                            }},
                        status=200
                    )
            return JsonResponse(
                    {"error": {
                        "code": "ABC",
                        "message": "ProductoId no encontrado",
                        "details": "Parámetro productId no encontrado en la base de datos"
                    }},
                status=404
            )
        
        else:
            return JsonResponse(
                    {"error": {
                        "code": "ABC",
                        "message": "Parámetros incorrectos",
                        "details": "productId incorrecto"
                    }},
                status=404
            )

def login(request):
    if request.method == "GET": 
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password") 
        if email is None or password is None :
            return JsonResponse(
                    {"error": {
                        "code": "ABC",
                        "message": "Falta información",
                        "details": "Falta información (name, minimunStock, quantity)"
                    }},
                status=400
            )
        user = next((u for u in users if u["email"] == email), None)
        if(user is None):
            return JsonResponse(
                    {"error": {
                        "code": "ABC",
                        "message": "Usuario no existe",
                        "details": "Usuario no encontrado en base de datos"
                    }},
                status=400
            )
        if bcrypt.checkpw(password.encode('utf-8'), user["password"]):
            pass
        else:
            return JsonResponse(
                    {"error": {
                        "code": "ABC",
                        "message": "Contraseña incorrecta",
                        "details": "Contraseña incorrecta"
                    }},
                status=400
            )
        token = jwt.encode({
            "id": user["id"],
            "name": user["name"],
            "exp": datetime.datetime.utcnow()+ datetime.timedelta(hours=1)
        }, JWT_SECRET, algorithm="HS256")
        return JsonResponse(
                {"success": {
                "code": "ABC",
                "message": "Login correcto",
                "token": token
            }},
            status=200
        )