from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS
from config import config

app = Flask(__name__)
CORS(app)

# Conexión a la base de datos
con = MySQL(app)

# Tabla Administradores
@app.route("/administradores", methods=['GET', 'POST'])
def administradores():
    if request.method == 'GET':
        try:
            cursor = con.connection.cursor()
            cursor.execute("SELECT * FROM administradores")
            datos = cursor.fetchall()

            administradores = [
                {"IdAdministrador": fila[0], "Nombre": fila[1], "Correo": fila[2], "Contrasena": fila[3]}
                for fila in datos
            ]
            return jsonify({"administradores": administradores, "mensaje": "Lista de administradores", "exito": True})
        except Exception as ex:
            return jsonify({"mensaje": f"Error: {ex}", "exito": False})

    elif request.method == 'POST':
        try:
            cursor = con.connection.cursor()
            nombre = request.json['Nombre']
            correo = request.json['Correo']
            contrasena = request.json['Contrasena']
            sql = "INSERT INTO administradores (Nombre, Correo, Contrasena) VALUES (%s, %s, %s)"
            cursor.execute(sql, (nombre, correo, contrasena))
            con.connection.commit()
            return jsonify({"mensaje": "Administrador agregado", "exito": True})
        except Exception as ex:
            return jsonify({"mensaje": f"Error: {ex}", "exito": False})

@app.route("/administradores/<int:id>", methods=['PUT', 'DELETE'])
def editar_eliminar_administrador(id):
    if request.method == 'PUT':
        try:
            cursor = con.connection.cursor()
            nombre = request.json['Nombre']
            correo = request.json['Correo']
            contrasena = request.json['Contrasena']
            sql = "UPDATE administradores SET Nombre = %s, Correo = %s, Contrasena = %s WHERE IdAdministrador = %s"
            cursor.execute(sql, (nombre, correo, contrasena, id))
            con.connection.commit()
            return jsonify({"mensaje": "Administrador actualizado", "exito": True})
        except Exception as ex:
            return jsonify({"mensaje": f"Error: {ex}", "exito": False})

    elif request.method == 'DELETE':
        try:
            cursor = con.connection.cursor()
            sql = "DELETE FROM administradores WHERE IdAdministrador = %s"
            cursor.execute(sql, (id,))
            con.connection.commit()
            return jsonify({"mensaje": "Administrador eliminado", "exito": True})
        except Exception as ex:
            return jsonify({"mensaje": f"Error: {ex}", "exito": False})
        
@app.route("/administradores/login", methods=['POST'])
def login_administrador():
    try:
        correo = request.json['Correo']
        contrasena = request.json['Contrasena']
        
        cursor = con.connection.cursor()
        sql = "SELECT * FROM administradores WHERE Correo = %s AND Contrasena = %s"
        cursor.execute(sql, (correo, contrasena))
        admin = cursor.fetchone()

        if admin:
            return jsonify({
                "mensaje": "Login exitoso",
                "exito": True,
                "administrador": {
                    "IdAdministrador": admin[0],
                    "Nombre": admin[1],
                    "Correo": admin[2]
                }
            })
        else:
            return jsonify({
                "mensaje": "Credenciales incorrectas",
                "exito": False
            })
    except Exception as ex:
        return jsonify({
            "mensaje": f"Error al autenticar administrador: {ex}",
            "exito": False
        })


# Tabla Escuela
@app.route("/escuelas", methods=['GET', 'POST'])
def escuelas():
    if request.method == 'GET':
        try:
            cursor = con.connection.cursor()
            cursor.execute("SELECT * FROM escuela")
            datos = cursor.fetchall()

            escuelas = [
                {
                    "IdEscuela": fila[0],
                    "Nombre": fila[1],
                    "Direccion": fila[2],
                    "Correo": fila[3],
                    "Telefono": fila[4],
                    "NumeroEscuela": fila[5],
                    "MetodoPago": fila[6],
                    "CantidadLicencias": fila[7],
                    "FechaExpiracion": fila[8]
                }
                for fila in datos
            ]
            return jsonify({"escuelas": escuelas, "mensaje": "Lista de escuelas", "exito": True})
        except Exception as ex:
            return jsonify({"mensaje": f"Error: {ex}", "exito": False})

    elif request.method == 'POST':
        try:
            cursor = con.connection.cursor()
            datos = (
                request.json['Nombre'],
                request.json['Direccion'],
                request.json['Correo'],
                request.json['Telefono'],
                request.json['NumeroEscuela'],
                request.json['MetodoPago'],
                request.json['CantidadLicencias'],
                request.json['FechaExpiracion']
            )
            sql = """INSERT INTO escuela (Nombre, Direccion, Correo, Telefono, NumeroEscuela, MetodoPago, CantidadLicencias, FechaExpiracion)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, datos)
            con.connection.commit()
            return jsonify({"mensaje": "Escuela agregada", "exito": True})
        except Exception as ex:
            return jsonify({"mensaje": f"Error: {ex}", "exito": False})

@app.route("/escuelas/<int:id>", methods=['PUT', 'DELETE'])
def editar_eliminar_escuela(id):
    if request.method == 'PUT':
        try:
            cursor = con.connection.cursor()
            datos = (
                request.json['Nombre'],
                request.json['Direccion'],
                request.json['Correo'],
                request.json['Telefono'],
                request.json['NumeroEscuela'],
                request.json['MetodoPago'],
                request.json['CantidadLicencias'],
                request.json['FechaExpiracion'],
                id
            )
            sql = """UPDATE escuela SET Nombre = %s, Direccion = %s, Correo = %s, Telefono = %s, 
                     NumeroEscuela = %s, MetodoPago = %s, CantidadLicencias = %s, FechaExpiracion = %s WHERE IdEscuela = %s"""
            cursor.execute(sql, datos)
            con.connection.commit()
            return jsonify({"mensaje": "Escuela actualizada", "exito": True})
        except Exception as ex:
            return jsonify({"mensaje": f"Error: {ex}", "exito": False})

    elif request.method == 'DELETE':
        try:
            cursor = con.connection.cursor()
            sql = "DELETE FROM escuela WHERE IdEscuela = %s"
            cursor.execute(sql, (id,))
            con.connection.commit()
            return jsonify({"mensaje": "Escuela eliminada", "exito": True})
        except Exception as ex:
            return jsonify({"mensaje": f"Error: {ex}", "exito": False})

#agregado el 02/12/2024
@app.route("/escuelas/verificar", methods=['POST'])
def verificar_escuela():
    try:
        nombre = request.json['Nombre']
        correo = request.json['Correo']
        numero_escuela = request.json['NumeroEscuela']
        
        cursor = con.connection.cursor()
        sql = "SELECT * FROM escuela WHERE Nombre = %s AND Correo = %s AND NumeroEscuela = %s"
        cursor.execute(sql, (nombre, correo, numero_escuela))
        escuela = cursor.fetchone()

        if escuela:
            return jsonify({
                "mensaje": "Escuela encontrada",
                "exito": True,
                "escuela": {
                    "IdEscuela": escuela[0],
                    "Nombre": escuela[1],
                    "Correo": escuela[3],
                    "NumeroEscuela": escuela[5]
                }
            })
        else:
            return jsonify({
                "mensaje": "No se encontró la escuela",
                "exito": False
            })
    except Exception as ex:
        return jsonify({
            "mensaje": f"Error al verificar escuela: {ex}",
            "exito": False
        })


# Tabla Alumno
@app.route("/alumnos", methods=['GET', 'POST'])
def alumnos():
    if request.method == 'GET':
        try:
            cursor = con.connection.cursor()
            cursor.execute("SELECT * FROM alumno")
            datos = cursor.fetchall()

            alumnos = [
                {"Matricula": fila[0], "Nombre": fila[1], "Escuela": fila[2], "Contacto": fila[3]}
                for fila in datos
            ]
            return jsonify({"alumnos": alumnos, "mensaje": "Lista de alumnos", "exito": True})
        except Exception as ex:
            return jsonify({"mensaje": f"Error: {ex}", "exito": False})

    elif request.method == 'POST':
        try:
            cursor = con.connection.cursor()
            datos = (
                request.json['Matricula'],
                request.json['Nombre'],
                request.json['Escuela'],
                request.json['Contacto']
            )
            sql = "INSERT INTO alumno (Matricula, Nombre, Escuela, Contacto) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, datos)
            con.connection.commit()
            return jsonify({"mensaje": "Alumno agregado", "exito": True})
        except Exception as ex:
            return jsonify({"mensaje": f"Error: {ex}", "exito": False})

@app.route("/alumnos/<string:matricula>", methods=['PUT', 'DELETE'])
def editar_eliminar_alumno(matricula):
    if request.method == 'PUT':
        try:
            cursor = con.connection.cursor()
            datos = (
                request.json['Nombre'],
                request.json['Escuela'],
                request.json['Contacto'],
                matricula
            )
            sql = "UPDATE alumno SET Nombre = %s, Escuela = %s, Contacto = %s WHERE Matricula = %s"
            cursor.execute(sql, datos)
            con.connection.commit()
            return jsonify({"mensaje": "Alumno actualizado", "exito": True})
        except Exception as ex:
            return jsonify({"mensaje": f"Error: {ex}", "exito": False})

    elif request.method == 'DELETE':
        try:
            cursor = con.connection.cursor()
            sql = "DELETE FROM alumno WHERE Matricula = %s"
            cursor.execute(sql, (matricula,))
            con.connection.commit()
            return jsonify({"mensaje": "Alumno eliminado", "exito": True})
        except Exception as ex:
            return jsonify({"mensaje": f"Error: {ex}", "exito": False})

        
# Tabla Padres
@app.route("/padres", methods=['GET', 'POST'])
def padres():
    if request.method == 'GET':
        try:
            cursor = con.connection.cursor()
            cursor.execute("SELECT * FROM padres")
            datos = cursor.fetchall()

            padres = [
                {"IdPadre": fila[0], "Nombre": fila[1], "Correo": fila[2], "Contrasena": fila[3], "MetodoPago": fila[4], "FechaExpiracion": fila[5]}
                for fila in datos
            ]
            return jsonify({"padres": padres, "mensaje": "Lista de padres", "exito": True})
        except Exception as ex:
            return jsonify({"mensaje": f"Error: {ex}", "exito": False})

    elif request.method == 'POST':
        try:
            cursor = con.connection.cursor()
            datos = (
                request.json['Nombre'],
                request.json['Correo'],
                request.json['Contrasena'],
                request.json['MetodoPago'],
                request.json['FechaExpiracion']
            )
            sql = """INSERT INTO padres (Nombre, Correo, Contrasena, MetodoPago, FechaExpiracion)
                     VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(sql, datos)
            con.connection.commit()
            return jsonify({"mensaje": "Padre agregado", "exito": True})
        except Exception as ex:
            return jsonify({"mensaje": f"Error: {ex}", "exito": False})

@app.route("/padres/<int:id>", methods=['PUT', 'DELETE'])
def editar_eliminar_padre(id):
    if request.method == 'PUT':
        try:
            cursor = con.connection.cursor()
            datos = (
                request.json['Nombre'],
                request.json['Correo'],
                request.json['Contrasena'],
                request.json['MetodoPago'],
                request.json['FechaExpiracion'],
                id
            )
            sql = """UPDATE padres SET Nombre = %s, Correo = %s, Contrasena = %s, MetodoPago = %s, 
                     FechaExpiracion = %s WHERE IdPadre = %s"""
            cursor.execute(sql, datos)
            con.connection.commit()
            return jsonify({"mensaje": "Padre actualizado", "exito": True})
        except Exception as ex:
            return jsonify({"mensaje": f"Error: {ex}", "exito": False})

    elif request.method == 'DELETE':
        try:
            cursor = con.connection.cursor()
            sql = "DELETE FROM padres WHERE IdPadre = %s"
            cursor.execute(sql, (id,))
            con.connection.commit()
            return jsonify({"mensaje": "Padre eliminado", "exito": True})
        except Exception as ex:
            return jsonify({"mensaje": f"Error: {ex}", "exito": False})

@app.route("/padres/login", methods=['POST'])
def login_padre():
    try:
        correo = request.json['Correo']
        contrasena = request.json['Contrasena']
        
        cursor = con.connection.cursor()
        sql = "SELECT * FROM padres WHERE Correo = %s AND Contrasena = %s"
        cursor.execute(sql, (correo, contrasena))
        padre = cursor.fetchone()

        if padre:
            return jsonify({
                "mensaje": "Login exitoso",
                "exito": True,
                "padre": {
                    "IdPadre": padre[0],
                    "Nombre": padre[1],
                    "Correo": padre[2]
                }
            })
        else:
            return jsonify({
                "mensaje": "Credenciales incorrectas",
                "exito": False
            })
    except Exception as ex:
        return jsonify({
            "mensaje": f"Error al autenticar padre: {ex}",
            "exito": False
        })


# Manejo de errores
def pagina_no_encontrada(error):
    return '<h1> La página que estás buscando no existe </h1>', 404

# Configuración y ejecución del servidor
if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(host='0.0.0.0', port=5000)
