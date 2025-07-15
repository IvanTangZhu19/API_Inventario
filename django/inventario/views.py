from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import datetime

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

def getProducts(request):
    if request.method == "GET":
        return JsonResponse(inventario, safe=False)