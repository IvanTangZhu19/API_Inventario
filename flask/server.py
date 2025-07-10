from flask import Flask, jsonify, request
import jwt
import datetime
import bcrypt

app = Flask(__name__)

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
        "lastUpdated": datetime.datetime.utcnow()
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
            i["lastUpdated"] = datetime.datetime.utcnow()
            return jsonify({
                "success": {
                    "code": "ABC",
                    "message": "Se actualizó correctamente",
                }
            }), 200
        else:
            return jsonify({
                "error": {
                    "code": "ABC",
                    "message": "ProductoId no encontrado",
                    "details": "Parámetro productId no encontrado en la base de datos"
                }
            }), 404 

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

@app.route("/users/login", methods=["GET"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password") 
    if email is None or password is None :
        return jsonify({
            "error": {
                "code": "ABC",
                "message": "Falta inforamción",
                "details": "Flata información email o password"
            }
        }), 400
    user = next((u for u in users if u["email"] == email), None)
    if(user is None):
         return jsonify({
            "error": {
                "code": "ABC",
                "message": "Usuario no existe",
                "details": "Usuario no encontrado en base de datos"
            }
        }), 400
    if bcrypt.checkpw(password.encode('utf-8'), user["password"]):
        pass
    else:
        return jsonify({
            "error": {
                "code": "ABC",
                "message": "Contraseña incorrecta",
                "details": "Contraseña incorrecta"
            }
        }), 400
    token = jwt.encode({
        "id": user["id"],
        "name": user["name"],
        "exp": datetime.datetime.utcnow()+ datetime.timedelta(hours=1)
    }, JWT_SECRET, algorithm="HS256")

    return jsonify({
        "success": {
            "code": "ABC",
            "message": "Login correcto",
            "token": token
        }
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=4002)