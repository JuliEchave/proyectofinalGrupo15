from flask import Flask ,jsonify ,request
# del modulo flask importar la clase Flask y los métodos jsonify,request
from flask_cors import CORS       # del modulo flask_cors importar CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
app=Flask(__name__)  # crear el objeto app de la clase Flask
CORS(app) #modulo cors es para que me permita acceder desde el frontend al backend

# configuro la base de datos, con el nombre el usuario y la clave
# app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://user:password@localhost/proyecto'
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root@localhost/proyecto'
# URI de la BBDD                          driver de la BD  user:clave@URLBBDD/nombreBBDD
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #none
db= SQLAlchemy(app)   #crea el objeto db de la clase SQLAlquemy
ma=Marshmallow(app)   #crea el objeto ma de de la clase Marshmallow


# defino la tabla
class Remera(db.Model):   # la clase Producto hereda de db.Model    
    id=db.Column(db.Integer, primary_key=True)   #define los campos de la tabla
    modelo=db.Column(db.String(100))
    talle=db.Column(db.String(10))
    stock=db.Column(db.Integer)
    precio=db.Column(db.Integer)
    imagen=db.Column(db.String(400))
    def __init__(self,modelo,talle,stock,precio,imagen):   #crea el  constructor de la clase
        self.modelo=modelo  # no hace falta el id porque lo crea sola mysql por ser auto_incremento
        self.talle=talle
        self.stock=stock
        self.precio=precio
        self.imagen=imagen




    #  si hay que crear mas tablas , se hace aqui




with app.app_context():
    db.create_all()  # aqui crea todas las tablas
#  ************************************************************
class RemeraSchema(ma.Schema):
    class Meta:
        fields=('id','modelo','talle','stock','precio','imagen')




remera_schema=RemeraSchema()            # El objeto producto_schema es para traer un producto
remeras_schema=RemeraSchema(many=True)  # El objeto productos_schema es para traer multiples registros de producto


# crea los endpoint o rutas (json)
@app.route('/remera',methods=['GET'])
def get_Remeras():
    all_remeras=Remera.query.all()         # el metodo query.all() lo hereda de db.Model
    result=remeras_schema.dump(all_remeras)  # el metodo dump() lo hereda de ma.schema y
                                                 # trae todos los registros de la tabla
    return jsonify(result)                       # retorna un JSON de todos los registros de la tabla




@app.route('/remera/<id>',methods=['GET'])      
def get_remera(id):
    remera=Remera.query.get(id)
    return remera_schema.jsonify(remera)   # retorna el JSON de un producto recibido como parametro




@app.route('/remera/<id>',methods=['DELETE'])
def delete_remeras(id):
    remera=remera.query.get(id)
    db.session.delete(remera)
    db.session.commit()
    return remera_schema.jsonify(remera)   # me devuelve un json con el registro eliminado


@app.route('/remera', methods=['POST']) # crea ruta o endpoint
def create_remera():
    #print(request.json)  # request.json contiene el json que envio el cliente
    modelo=request.json['modelo']
    talle=request.json['talle']
    stock=request.json['stock'] 
    precio=request.json['precio']
    imagen=request.json['imagen']
    new_remera=Remera(modelo,talle,stock,precio,imagen)
    db.session.add(new_remera)
    db.session.commit()
    return remera_schema.jsonify(new_remera)


@app.route('/remera/<id>' ,methods=['PUT'])
def update_remeras(id):
    remera=Remera.query.get(id)
 
    remera.modelo=request.json['modelo']
    remera.talle=request.json['talle']
    remera.stock=request.json['stock']
    remera.precio=request.json['precio']
    remera.imagen=request.json['imagen']


    db.session.commit()
    return remera_schema.jsonify(remera)
 


# programa principal *******************************
if __name__=='__main__':  
    app.run(debug=True, port=5000)    # ejecuta el servidor Flask en el puerto 5000