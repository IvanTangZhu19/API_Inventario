from flask import Flask, jsonify
import json

app = Flask(__name__)

inventario = [
    {
        "productId": 1,
        "name": "Manzana",
        "currentStock": 2,
        "minimunStock": 1,
        "lastUpdated": ""
    },
    {
        "productId": 2,
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


@app.route("/inventory")
def inventory():
    return jsonify({inventario}), 200

if __name__ == '__main__':
    app.run(debug=True, port=4002)