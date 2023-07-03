import hashlib
from getpass import getpass
from flask import Flask, request
import sqlite3

# Crear la base de datos SQLite y tabla para almacenar usuarios
conn = sqlite3.connect('usuarios.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS usuarios
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              nombre TEXT NOT NULL,
              password TEXT NOT NULL)''')
conn.commit()

# Función para almacenar usuarios y contraseñas en hash
def almacenar_usuario(nombre, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    c.execute("INSERT INTO usuarios (nombre, password) VALUES (?, ?)",
              (nombre, hashed_password))
    conn.commit()

# Función para validar usuarios
def validar_usuario(nombre, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    c.execute("SELECT * FROM usuarios WHERE nombre=? AND password=?",
              (nombre, hashed_password))
    return c.fetchone() is not None

# Crear la aplicación web con Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'Sitio web de ejemplo'

@app.route('/login', methods=['POST'])
def login():
    nombre = request.form.get('nombre')
    password = request.form.get('password')
    if validar_usuario(nombre, password):
        return 'Inicio de sesión exitoso'
    else:
        return 'Nombre de usuario o contraseña incorrectos'

if __name__ == '__main__':
    # Pedir los nombres de los usuarios y las contraseñas
    num_usuarios = int(input("Ingrese la cantidad de usuarios que desea registrar: "))
    usuarios = []
    contraseñas = []
    for i in range(num_usuarios):
        usuario = input(f"Ingrese el nombre del usuario {i+1}: ")
        contraseña = getpass(f"Ingrese la contraseña para {usuario}: ")
        usuarios.append(usuario)
        contraseñas.append(contraseña)

    # Almacenar los usuarios y contraseñas en hash
    for usuario, contraseña in zip(usuarios, contraseñas):
        almacenar_usuario(usuario, contraseña)
    # Mostrar los registros de usuarios después de agregarlos
    print("Registros de usuarios:")
    c.execute("SELECT * FROM usuarios")
    registros = c.fetchall()
    for registro in registros:
        print(f"Nombre: {registro[1]}")
        print(f"Hash de contraseña: {registro[2]}")
        print()

    # Ejecutar la aplicación en el puerto 4850
    app.run(port=4850)
