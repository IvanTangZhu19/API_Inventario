const express = require('express');

server = express();

server.use(express.json());

var productID = 2

var inventario = [
    {
        productId: 1,
        name: "Manzana",
        currentStock: 2,
        minimunStock: 1,
        lastUpdated: new Date().toISOString().slice(0, 10)
    },
    {
        productId: 2,
        name: "Mango",
        currentStock: 5,
        minimunStock: 2,
        lastUpdated: new Date().toISOString().slice(0, 10)
    }
];

server.get('/inventory', (req, res) => {
    res.status(200).json(inventario)
});

server.post('/inventory', (req, res) => {
    const { name, minimunStock, quantity, operation } = req.body;
    if (!name && !minimunStock && !quantity && !operation)
        return res.status(400).json({
            error: {
                code: "ABC",
                message: "Falta información",
                details: "Falta información (name, minimunStock, quantity, operation)"
            }
        })
    if (minimunStock < 0 || quantity < 0)
        return res.status(400).json({
            error: {
                code: "ABC",
                message: "Cantidades deben ser mayores a cero",
                details: "Cantidades: minimunStock, quantity deben ser mayores a cero"
            }
        })

    productID++
    inventario.push({
        productId: productID,
        name: name,
        currentStock: quantity,
        minimunStock: minimunStock,
        lastUpdated: new Date().toISOString().slice(0, 10)
    })
    return res.status(200).json({
        success: {
            code: "ABC",
            message: "Se añadió correctamente",
        }
    })
});

server.get('/inventory/:productId', (req, res) => {
    const productId = req.params.productId;
    if (productId != null) {
        for (var i = 0; i < inventario.length; i++) {
            if (inventario[i].productId == productId) {
                return res.status(200).json(inventario[i]);
            }
        }
        return res.status(404).json({
            error: {
                code: "ABC",
                message: "ProductoId no encontrado",
                details: "Parámetro productId no encontrado en la base de datos"
            }
        });
    } else res.status(400).json({
        error: {
            code: "ABC",
            message: "Parámetros incorrectos",
            details: "productId incorrecto"
        }
    });
});

server.put('/inventory/:productId', (req, res) => {
    const productId = req.params.productId;
    const { quantity, operation, name } = req.body;
    if ((productId != null || quantity > 0) &&
        (operation == "add" || operation == "substract")) {
        for (var i = 0; i < inventario.length; i++) {
            if (inventario[i].productId == productId) {
                if (operation == "substract" && inventario[i].currentStock >= quantity)
                    inventario[i].currentStock -= quantity;
                else if (operation == "substract" && inventario[i].currentStock < quantity)
                    return res.status(400).json({
                        error: {
                            code: "ABC",
                            message: "Cantidad erronea",
                            details: "Parámetro quantity es mayor que currentStock"
                        }
                    });
                else if (operation == "add") inventario[i].currentStock += quantity;
                else return res.status(500).json({
                    error: {
                        code: "ABC",
                        message: "Parámetros incorrectos",
                        details: "Algún parámetro (productId, quantity o operation) no cumple las validaciones"
                    }
                });
                inventario[i].lastUpdated = new Date().toISOString().slice(0, 10);
                if(name) inventario[i].name = name
                return res.status(200).json(
                    {
                        message: "ProductId " + productId + " actualizado correctamente"
                    }
                );
            }
        }
        return res.status(404).json({
            error: {
                code: "ABC",
                message: "ProductoId no encontrado",
                details: "Parámetro productId no encontrado en la base de datos"
            }
        });
    } else res.status(400).json({
        error: {
            code: "ABC",
            message: "Parámetros incorrectos",
            details: "Algún parámetro (productId, quantity o operation) no cumple las validaciones"
        }
    });
});

const port = 4002;
server.listen(port, () => {
    console.log(`La aplicación está escuchando en http://localhost:${port}`);
});