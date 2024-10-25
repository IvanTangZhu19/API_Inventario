const express = require('express');

server = express();

server.use(express.json());

var inventario = [
    {
        productId : 1,
        name: "Manzana",
        currentStock: 2,
        minimunStock: 1,
        lastUpdated: ""
    },
    {
        productId : 2,
        name: "Mango",
        currentStock: 5,
        minimunStock: 2,
        lastUpdated: ""
    }
];

server.get('/inventory/:productId', (req, res) => {
    const productId = req.params.productId;
    if(!productId || productId > 0){
        for(var i=0; i< inventario.length; i++){
            if(inventario[i].productId == productId) {
                return res.status(200).json(inventario[i]);
            }
        }
        res.status(404).json({message: "ProductId " + productId + " no encontrado"});
    } else res.status(400).json({
        message: "ProductId incorrecto"
    });
});

server.put('/inventory/:productId', (req, res) => {
    const productId = req.params.productId;
    const {quantity, operation } = req.body;
    if((!productId || productId > 0 || quantity > 0) && 
        (operation == "add" || operation == "substract")){
        for(var i=0; i< inventario.length; i++){
            if(inventario[i].productId == productId) {
                if(operation == "substract" && inventario[i].currentStock >= quantity) 
                    inventario[i].currentStock -= quantity;
                else if(operation == "substract" && inventario[i].currentStock < quantity) 
                    return res.status(200).json({message: "Cantidad mayor que el actual"});
                else if(operation == "add") inventario[i].currentStock += quantity;
                else return res.status(500).json({message: "error"});
                return res.status(200).json(
                    {message: "ProductId " +productId +" actualizado correctamente"}
                );
            }
        }
        res.status(404).json({message: "ProductId " + productId + " no encontrado"});
    } else res.status(400).json({
        message: "Datos incorrectos"
    });
});

const port = 4002;
server.listen(port, () => {
  console.log(`La aplicación está escuchando en http://localhost:${port}`);
});