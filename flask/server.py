from flask import Flask, jsonify, request
import json

app = Flask(__name__)

productID_ =2

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

@app.route("/inventory", methods=["POST"])
def createProduct():
    global productID_
    data = request.get_json()
    name = data.get("name")
    minimunStock = data.get("minimunStock")
    quantity = data.get("quantity") 
    if (name is None or minimunStock is None or quantity is None) :
        return jsonify({
            "error": {
                "code": "ABC",
                "message": "Falta información",
                "details": "Falta información (name, minimunStock, quantity)"
            }
        }), 400
    if (minimunStock < 0 or quantity < 0) :
        return jsonify({
            "error": {
                "code": "ABC",
                "message": "Cantidades deben ser mayores a cero",
                "details": "Cantidades: minimunStock, quantity deben ser mayores a cero"
            }
        }), 400
    productID_ = productID_ + 1
    inventario.append({
        "productID": productID_,
        "name": name,
        "quantity": quantity,
        "minimunStock": minimunStock,
        "lastUpdated": ""
    })
    return jsonify({
        "success": {
            "code": "ABC",
            "message": "Se añadió correctamente",
        }
    }), 201

@app.route("/inventory/<int:productID>", methods=["PUT"])
def updateProduct(productID):
    data = request.get_json()
    name = data.get("name")
    quantity = data.get("quantity") 
    operation = data.get("operation") 
    if (name is None or quantity is None or operation is None) :
        return jsonify({
            "error": {
                "code": "ABC",
                "message": "Falta información",
                "details": "Falta información (name, quantity, operation)"
            }
        }), 400
    if quantity <= 0 :
        return jsonify({
            "error": {
                "code": "ABC",
                "message": "Información incorrecta",
                "details": "Quantity debe ser mayor a cero"
            }
        }), 400
    if(operation != "add" and operation != "substract"):
        return jsonify({
            "error": {
                "code": "ABC",
                "message": "Información incorrecta",
                "details": "Operation tiene que ser add o substract"
            }
        }), 400
    for i in inventario:
        if (i["productID"] == productID) :
            if (operation == "substract" and i["currentStock"] >= quantity):
                i["currentStock"] -= quantity
            elif (operation == "substract" and i["currentStock"] < quantity):
                return jsonify({
                    "error": {
                        "code": "ABC",
                        "message": "Cantidad erronea",
                        "details": "No hay suficientes existencias del producto"
                    }
                }), 400
            elif (operation == "add"):
                i["currentStock"] += quantity
            i["name"] = name
            return jsonify({
                "success": {
                    "code": "ABC",
                    "message": "Se actualizó correctamente",
                }
            }), 200

@app.route("/inventory/<int:productID>", methods=["DELETE"])
def deleteProductByID(productID):
    if (productID is not None):
        for i in inventario:
            if i["productID"] == productID :
                inventario.remove(i)
                return jsonify({
                    "success": {
                        "code": "ABC",
                        "message": "Se eliminó correctamente",
                    }
                }), 200
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