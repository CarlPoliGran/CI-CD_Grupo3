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

# endpoint creacion de usuarios -----------------------------------------
# crear un usuario
@app.route('/create_user', methods=['POST'])
def create_user():
    user_data = request.json
    # Verificar los campos
    if 'identificacion' not in user_data or 'nombre' not in user_data or 'apellidos'  not in user_data or 'email' not in user_data or 'telefono' not in user_data:
        return 'Faltan campos requeridos (identificacion, nombre, apellidos, email, telefono)\n', 400 
    # Insertar
    collection.insert_one(user_data)
    return 'usuario creado correctamente\n' , 201

# endpoint creacion partida fiscal------------------------------------------
# crear una partida fiscal

#Crear la coleccion
collectionPart = db.partidas_db

@app.route('/partida_create', methods=['POST'])
def partida_create():
    user_data = request.json
    print("Datos recibidos:", user_data)

    # Verificar los campos requeridos
    required_fields = ['identificacionBuscar', 'fecha', 'nit', 'nombreComercio', 'itemDescripcion', 'subtotal', 'total', 'codigo']
    missing_fields = [field for field in required_fields if field not in user_data]
    if missing_fields:
        return jsonify({'error': f'Faltan campos requeridos: {", ".join(missing_fields)}'}), 400

    # Convertir tipos de datos
    try:
        identificacionBuscar = user_data['identificacionBuscar']
        fecha = user_data['fecha']
        nit = user_data['nit']
        nombreComercio = user_data['nombreComercio']
        itemDescripcion = user_data['itemDescripcion']
        subtotal = float(user_data['subtotal'])
        total = float(user_data['total'])
        codigo = int(user_data['codigo'])
    except ValueError as e:
        return jsonify({'error': f'Error en la conversión de tipos de datos: {e}'}), 400

    # Verificar que la id del usuario existe
    if not collection.find_one({'identificacion': identificacionBuscar}):
        return jsonify({'error': f'La identificacion {identificacionBuscar} no existe, ¡Verifique o registre primero el cliente!'}), 400

    # Crear el nuevo documento
    new_data = {
        'identificacion': identificacionBuscar,
        'fecha': fecha,
        'nit': nit,
        'nombreComercio': nombreComercio,
        'itemDescripcion': itemDescripcion,
        'subtotal': subtotal,
        'total': total,
        'codigo': codigo
    }

    # Insertar el nuevo documento
    collectionPart.insert_one(new_data)
    return jsonify({'message': 'Partida Fiscal registrada correctamente'}), 201


#endpoint retornar partidas fiscales de una identificacion---------------------------------------------
#retorna partidas fiscales
@app.route('/partidas/<identificacionCliente>', methods=['GET'])
def get_partidas(identificacionCliente):
    # Verificar que la identificación del usuario existe
    if not collection.find_one({'identificacion': identificacionCliente}):
        return jsonify({'error': f'La identificación {identificacionCliente} no existe, ¡Verifique o registre primero el cliente!'}), 400

    #partidas fiscales asociadas a la identificación
    partidas = list(collectionPart.find({'identificacion': identificacionCliente}, {'_id': 0}))
    #total de todas las partidas
    total_partidas = sum(partida['total'] for partida in partidas)

    response = {
        'partidas': partidas,
        'total_partidas': total_partidas
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')











