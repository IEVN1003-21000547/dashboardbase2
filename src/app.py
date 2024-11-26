from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS
from config import config

app = Flask(__name__)
CORS(app)

# Conexión a la base de datos
con = MySQL(app)

# Rutas
@app.route("/usuarios", methods=['GET'])
def lista_usuarios():
    """
    Lista todos los usuarios de la base de datos.
    """
    try:
        cursor = con.connection.cursor()
        sql = "SELECT * FROM usuarios"
        cursor.execute(sql)
        datos = cursor.fetchall()
        
        usuarios = []
        for fila in datos:
            usuario = {
                "idUsuario": fila[0],
                "nombre": fila[1],
                "correo": fila[2],
                "tipo": fila[3],
                "edad": fila[4]
            }
            usuarios.append(usuario)
        return jsonify({"usuarios": usuarios, "mensaje": "Lista de usuarios", "exito": True})
    except Exception as ex:
        return jsonify({"mensaje": f"Error al conectar a la base de datos: {ex}", "exito": False})
    
# Eliminar usuario
@app.route("/usuarios/<int:id>", methods=['DELETE'])
def eliminar_usuario(id):
    try:
        cursor = con.connection.cursor()
        sql = "DELETE FROM usuarios WHERE idUsuario = %s"  # Cambiado id a idUsuario para coincidir con tu esquema
        cursor.execute(sql, (id,))
        con.connection.commit()
        cursor.close()
        return jsonify({"message": "Usuario eliminado", 'exito': True})
    except Exception as ex:
        return jsonify({"message": f"Error al eliminar usuario: {ex}", 'exito': False})


@app.route("/usuarios", methods=['POST'])
def agregar_usuario():
    try:
        cursor = con.connection.cursor()
        nombre = request.json['nombre']
        correo = request.json['correo']
        tipo = request.json['tipo']
        edad = request.json['edad']
        password = request.json['password']

        # Asegúrate que los nombres de columnas coincidan con tu base de datos
        sql = """INSERT INTO usuarios (nombre, correo, tipo, edad, password) 
                 VALUES (%s, %s, %s, %s, %s)"""
        datos = (nombre, correo, tipo, edad, password)
        cursor.execute(sql, datos)
        con.connection.commit()
        cursor.close()

        return jsonify({
            "mensaje": "Usuario agregado correctamente", 
            "exito": True
        })
    except Exception as ex:
        return jsonify({
            "mensaje": f"Error al agregar el usuario: {str(ex)}", 
            "exito": False
        })

@app.route("/usuario/<int:idUsuario>", methods=['DELETE'])
def borrar_usuario(idUsuario):
    """
    Borra un usuario de la base de datos por su ID.
    """
    try:
        cursor = con.connection.cursor()
        sql = "DELETE FROM usuarios WHERE idUsuario = %s"
        cursor.execute(sql, (idUsuario,))
        con.connection.commit()
        
        return jsonify({"mensaje": "Usuario eliminado correctamente", "exito": True})
    except Exception as ex:
        return jsonify({"mensaje": f"Error al eliminar el usuario: {ex}", "exito": False})


# Manejo de errores
def pagina_no_encontrada(error):
    return '<h1> La página que estás buscando no existe </h1>', 404

# Configuración y ejecución del servidor
if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(host='0.0.0.0', port=5000)
