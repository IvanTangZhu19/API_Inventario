from flask import Flask, jsonify
import json

app = Flask(__name__)

inventario = [
    {
        "productID": 1,
        "name": "Manzana",
        "currentStock": 2,
        "minimunStock": 1,
        "lastUpdated": ""
    },
    {
        "productID": 2,
        "name": "Mango",
        "currentStock": 5,
        "minimunStock": 2,
        "lastUpdated": ""
    }
]

users = [
    {
        "id": 1,
        "name": "Iván",
        "email": "ivan@gmail.com",
        "password": ""
    }
]


@app.route("/inventory", methods=["GET"])
def getProducts():
    return jsonify(inventario), 200

@app.route("/inventory/<int:productID>", methods=["GET"])
def getProductsByID(productID):
    if (productID is not None):
        for i in inventario:
            if i["productID"] == productID :
                return jsonify(i), 200
        return jsonify({
            "error": {
                "code": "ABC",
                "message": "ProductoId no encontrado",
                "details": "Parámetro productId no encontrado en la base de datos"
            }
        }), 404 
    else:
        return jsonify({
            "error": {
                "code": "ABC",
                "message": "Parámetros incorrectos",
                "details": "productId incorrecto"
            }
        }), 400 

if __name__ == '__main__':
    app.run(debug=True, port=4002)