import socket
import threading
import string
import random
import json

users = {
    "VE0001ABC": {
        "email": "sant@gmail.com",
        "user": "sant04",
        "password": "12345",
        "linked_devices": ["VE0002DEF"],
    },
    "VE0002DEF": {
        "email": "acness@hotmail.com",
        "user": "acness08",
        "password": "67890",
        "linked_devices": ["VE0001ABC", "VE0003GHI"],
    },
    "VE0003GHI": {
        "email": "sidness@example.com",
        "user": "sidness26",
        "password": "98765",
        "linked_devices": ["VE0001ABC"],
    },
}


def generate_user_id(pais="VE"):
    nums = "".join(random.choices(string.ascii_uppercase, k=4))
    ch = "".join(random.choices(string.digits, k=4))
    return f"{pais}{nums}{ch}"


def register_new_user(email, user, password):
    asignedId = generate_user_id()
    if asignedId in users:
        register_new_user(email, user, password)
    users[asignedId] = {"email": email, "user": user, "password": password}
    print(users)


def validate_user(user, password):
    for userId, user_data in users.items():
        if user == user_data["user"] and password == user_data["password"]:
            print("Inicio de sesión exitoso")
            return userId  # Devuelves el ID del usuario
        elif user == user_data["user"]:
            print("La contraseña es incorrecta.")
            return None
    print("El usuario ingresado no existe.")
    return None


def link_device(user_id, linked_user_id):
    if user_id in users:
        if "linked_devices" not in users[user_id]:
            users[user_id]["linked_devices"] = []
        if linked_user_id not in users[user_id]["linked_devices"]:
            users[user_id]["linked_devices"].append(linked_user_id)
        else:
            print(
                f"El dispositivo {linked_user_id} ya está vinculado con el usuario {user_id}."
            )
    else:
        print(f"Usuario {user_id} no encontrado.")


def get_user_data(user_id):
    return {"id": user_id, "user": users[user_id]["user"]} if user_id in users else None


def connect_to_server(logged_in_user_id, page):
    try:
        server_ip = "127.0.0.1"  # Reemplaza con la IP del servidor si es necesario
        server_port = 5051  # Puerto del servidor
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))
        print(f"Conectado al servidor en {server_ip}:{server_port}")

        # Enviar solo el user_id al servidor
        user_data = {"userId": logged_in_user_id}
        client_socket.send(json.dumps(user_data).encode())

        # Mantener la conexión abierta
        while True:
            data = client_socket.recv(1024)
            if not data:
                break

    except Exception as ex:
        print(f"Error al conectar al servidor: {ex}")
    finally:
        client_socket.close()


def connect_to_server_threaded(logged_in_user_id, page):
    threading.Thread(target=connect_to_server, args=(logged_in_user_id, page)).start()