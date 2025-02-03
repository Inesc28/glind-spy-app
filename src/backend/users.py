import random
import string

# Datos de prueba para comprobar si la validacion funcionaba (ideal para pruebas)
email_list = ["sant@gmail.com", "acness@hotmail.com", "sidness@example.com"]
user_list = ["sant04", "acness08", "sidness26"]
user_id_list = ["VE0001ABC", "VE0002DEF", "VE0003GHI"]
password_list = ["12345", "67890", "98765"]

# Funcion que genera el id de usuario
def generate_user_id(pais="VE"):
    nums = ''.join((random.choices(string.ascii_uppercase, k=4)))
    ch = ''.join((random.choices(string.digits, k=4)))
    return f"{pais}{nums}{ch}"


# Funcion que guarda los datos en las listas, es llamada en el register
def save_data(email, user, password):

    email_list.append(email)
    user_list.append(user)
    password_list.append(password)
    user_id_list.append(generate_user_id())
    print(email_list)
    print(user_list)
    print(password_list)
    print("Usuario registrado con exito!")


# Funcion que valida los datos, es llamada en el login
def validate_user(user, password):
    if user in user_list:
        index = user_list.index(user)
        if password == password_list[index]:
            print("Inicio de sesión exitoso")
            return True
        else:
            print("La contraseña es incorrecta.")
            return False
    else:
        print("El usuario no existe.")
        return False
