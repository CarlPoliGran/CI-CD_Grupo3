#Importar dependencias
from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
from bson import ObjectId  

app = Flask(__name__)
#implementar CORS para los request de otros dominios
CORS(app)

# Credenciales y datos de conexión
mongo_host = 'dbfacturacion'
mongo_port = 27017
mongo_user = 'carlos'
mongo_password = '123'  
mongo_db = 'dbfacturacion'

# Construir la URI de conexión con las credenciales
mongo_uri = f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}/{mongo_db}?authSource=admin"

# Conexión a la base de datos Mongo
client = MongoClient(mongo_uri)
db = client[mongo_db]
#creacion de la colección de usuarios
collection = db.usuarios_db

#metodo prueba creación manual docker
@app.route('/prueba', methods=['GET'])
def prueba():
    return "Prueba de conexión satisfactoria"

# crear un usuario
@app.route('/create_user', methods=['POST'])
def create_user():
                #json de la solicitud
    user_data = request.json
    # Verificar los campos
    if 'nombre' not in user_data or 'apellido' not in user_data or 'telefono' not in user_data:
        return 'Faltan campos requeridos (nombre, apellido, telefono)\n', 400 
    # Insertar usuario en la coleccion
    collection.insert_one(user_data)
    return 'usuario creado correctamente\n'


# obtener todas las facturas
@app.route('/get_users', methods=['GET'])
def get_users():
    #arreglo para los usuarios de la colección
    users = []
    for user in collection.find():
        #convertir el id en un string
        user['_id'] = str(user['_id'])
        #agregar el usuario al arreglo
        users.append(user)
        #retorna un json con el arreglo de usuarios
    return jsonify(users)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')