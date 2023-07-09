import os
import subprocess

# Ruta del archivo de registro
REGISTRO = "/home/devasc/Documents/registro.txt"

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu_principal():
    limpiar_pantalla()
    print("======== BIENVENIDO ADMIN LINUX ========")
    print("a. Administración de usuarios")
    print("b. Administración de archivos")
    print("c. Salir")

def mostrar_menu_usuarios():
    limpiar_pantalla()
    print("======== ADMIN USUARIOS ========")
    print("a. Crear usuario")
    print("b. Eliminar usuario")
    print("c. Volver")

def mostrar_menu_archivos():
    limpiar_pantalla()
    print("======== ADMIN ARCHIVOS ========")
    print("a. Crear archivo")
    print("b. Eliminar archivo")
    print("c. Volver")

def verificar_existencia(nombre, tipo):
    if not os.path.isfile(REGISTRO):
        return False
    with open(REGISTRO, "r") as archivo:
        lineas = archivo.readlines()
        for linea in lineas:
            nombre_existente, tipo_existente = linea.strip().split(":")
            if nombre == nombre_existente and tipo == tipo_existente:
                return True
    return False

def registrar(nombre, tipo):
    with open(REGISTRO, "a") as archivo:
        archivo.write("{}:{}\n".format(nombre, tipo))

def crear_usuario():
    nombre_usuario = input("Ingrese nombre de usuario a crear: ")
    if len(nombre_usuario) > 10:
        print("Error: El nombre de usuario debe tener máximo 10 caracteres.")
    elif not nombre_usuario.isalpha():
        print("Error: El nombre de usuario solo puede contener letras.")
    elif verificar_existencia(nombre_usuario, "usuario"):
        print("Error: El usuario ya está registrado.")
    else:
        # Verificar si el usuario ya existe en el sistema
        try:
            subprocess.run(["id", nombre_usuario], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("Error: El usuario ya existe en el sistema.")
        except subprocess.CalledProcessError:
            # Crear el usuario real utilizando el comando 'useradd'
            try:
                subprocess.run(["sudo", "useradd", nombre_usuario], check=True)
                registrar(nombre_usuario, "usuario")
                print("Usuario {} creado exitosamente.".format(nombre_usuario))
            except subprocess.CalledProcessError as e:
                print("Error al crear el usuario: ", e)

def eliminar_usuario():
    nombre_usuario = input("Ingrese nombre de usuario a eliminar: ")
    if len(nombre_usuario) > 10:
        print("Error: El nombre de usuario debe tener máximo 10 caracteres.")
    elif not nombre_usuario.isalpha():
        print("Error: El nombre de usuario solo puede contener letras.")
    elif verificar_existencia(nombre_usuario, "usuario"):
        # Eliminar el usuario real utilizando el comando 'userdel'
        try:
            subprocess.run(["sudo", "userdel", nombre_usuario], check=True)
            lineas = []
            with open(REGISTRO, "r") as archivo:
                lineas = archivo.readlines()
            with open(REGISTRO, "w") as archivo:
                for linea in lineas:
                    nombre_existente, tipo_existente = linea.strip().split(":")
                    if nombre_usuario != nombre_existente or tipo_existente != "usuario":
                        archivo.write(linea)
            print("Usuario {} eliminado exitosamente.".format(nombre_usuario))
        except subprocess.CalledProcessError as e:
            print("Error al eliminar el usuario: ", e)
    else:
        print("Error: El usuario no existe.")

def crear_archivo():
    nombre_archivo = input("Ingrese nombre de archivo a crear: ")
    if len(nombre_archivo) > 10:
        print("Error: El nombre de archivo debe tener máximo 10 caracteres.")
    elif not nombre_archivo.isalpha():
        print("Error: El nombre de archivo solo puede contener letras.")
    elif verificar_existencia(nombre_archivo, "archivo"):
        print("Error: El archivo ya está registrado.")
    else:
        extension = input("Ingrese la extensión del archivo (txt, pdf, docx, xlsx): ")
        if extension not in ["txt", "pdf", "docx", "xlsx"]:
            print("Error: Extensión de archivo no válida.")
        else:
            registrar(nombre_archivo, "archivo")
            print("Archivo {} creado exitosamente.".format(nombre_archivo + "." + extension))

def eliminar_archivo():
    nombre_archivo = input("Ingrese nombre de archivo a eliminar: ")
    if len(nombre_archivo) > 10:
        print("Error: El nombre de archivo debe tener máximo 10 caracteres.")
    elif not nombre_archivo.isalpha():
        print("Error: El nombre de archivo solo puede contener letras.")
    elif verificar_existencia(nombre_archivo, "archivo"):
        lineas = []
        with open(REGISTRO, "r") as archivo:
            lineas = archivo.readlines()
        with open(REGISTRO, "w") as archivo:
            for linea in lineas:
                nombre_existente, tipo_existente = linea.strip().split(":")
                if nombre_archivo != nombre_existente or tipo_existente != "archivo":
                    archivo.write(linea)
        print("Archivo {} eliminado exitosamente.".format(nombre_archivo))
    else:
        print("Error: El archivo no existe.")

def administrar_usuarios():
    while True:
        mostrar_menu_usuarios()
        opcion = input("Seleccione una opción: ")
        if opcion == "a":
            crear_usuario()
        elif opcion == "b":
            eliminar_usuario()
        elif opcion == "c":
            break
        else:
            print("Opción no válida.")

def administrar_archivos():
    while True:
        mostrar_menu_archivos()
        opcion = input("Seleccione una opción: ")
        if opcion == "a":
            crear_archivo()
        elif opcion == "b":
            eliminar_archivo()
        elif opcion == "c":
            break
        else:
            print("Opción no válida.")

def administrar_linux():
    if os.path.isfile(REGISTRO):
        with open(REGISTRO, "r") as archivo:
            lineas = archivo.readlines()
            for linea in lineas:
                nombre_existente, tipo_existente = linea.strip().split(":")
                if tipo_existente == "usuario":
                    print("Usuario {} ya registrado.".format(nombre_existente))

    while True:
        mostrar_menu_principal()
        opcion = input("Seleccione una opción: ")
        if opcion == "a":
            administrar_usuarios()
        elif opcion == "b":
            administrar_archivos()
        elif opcion == "c":
            break
        else:
            print("Opción no válida.")

administrar_linux()
