import os
import subprocess

def check_for_updates():
    if os.name != "posix":
        return False
    try:
        subprocess.check_output(['apt', 'list', '--upgradable'])
        return True
    except subprocess.CalledProcessError:
        return False

def prompt_user_to_install_update():
    print("Existen actualizaciones disponibles para el sistema operativo devasc.")
    print("¿Desea instalarlas ahora?")
    print("(S)i o (N)o")
    choice = input()

    return choice.lower() == 's'

def install_update():
    try:
        subprocess.run(['apt', 'upgrade', '-y'])
        print("Las actualizaciones se han instalado correctamente.")
    except subprocess.CalledProcessError as e:
        print("Se produjo un error al instalar las actualizaciones:", e)

def main():
    if check_for_updates():
        if prompt_user_to_install_update():
            install_update()
    else:
        print("No hay actualizaciones disponibles.")

if __name__ == "__main__":
    main()

