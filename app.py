from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/proyecto'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Remera(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    modelo = db.Column(db.String(100))
    talle = db.Column(db.String(10))
    stock = db.Column(db.Integer)
    precio = db.Column(db.Integer)
    imagen = db.Column(db.String(400))

    def __init__(self, modelo, talle, stock, precio, imagen):
        self.modelo = modelo
        self.talle = talle
        self.stock = stock
        self.precio = precio
        self.imagen = imagen


class RemeraSchema(ma.Schema):
    class Meta:
        fields = ('id', 'modelo', 'talle', 'stock', 'precio', 'imagen')


remera_schema = RemeraSchema()
remeras_schema = RemeraSchema(many=True)


@app.route('/remera', methods=['GET'])
def get_Remeras():
    all_remeras = Remera.query.all()
    result = remeras_schema.dump(all_remeras)
    return jsonify(result)


@app.route('/remera/<id>', methods=['GET'])
def get_remera(id):
    remera = Remera.query.get(id)
    return remera_schema.jsonify(remera)


@app.route('/remera/<id>', methods=['DELETE'])
def delete_remeras(id):
    remera = Remera.query.get(id)
    db.session.delete(remera)
    db.session.commit()
    return jsonify(message='Remera eliminada con exito!')


@app.route('/remera', methods=['POST'])
def create_remera():
    modelo = request.json['modelo']
    talle = request.json['talle']
    stock = request.json['stock']
    precio = request.json['precio']
    imagen = request.json['imagen']
    new_remera = Remera(modelo, talle, stock, precio, imagen)
    db.session.add(new_remera)
    db.session.commit()
    return remera_schema.jsonify(new_remera)


@app.route('/remera/<id>', methods=['PUT'])
def update_remeras(id):
    remera = Remera.query.get(id)

    remera.modelo = request.json['modelo']
    remera.talle = request.json['talle']
    remera.stock = request.json['stock']
    remera.precio = request.json['precio']
    remera.imagen = request.json['imagen']

    db.session.commit()
    return remera_schema.jsonify(remera)

if __name__=='__main__':  
    app.run(debug=True, port=5000)    # ejecuta el servidor Flask en el puerto 5000
