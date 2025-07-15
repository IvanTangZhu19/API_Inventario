from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import datetime
import json

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