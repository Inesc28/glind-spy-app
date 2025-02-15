import socket
import threading
import json
from users import link_device

# Diccionario global para almacenar conexiones
connections = {}


# Función para manejar la conexión de cada cliente
def handle_client(conn, addr):
    print(f"Conexión establecida desde {addr}")
    data = conn.recv(1024).decode()
    if data:
        user_data = json.loads(data)
        user_id = user_data["userId"]
        device_type = user_data["deviceType"]

        # Almacenar la conexión del cliente
        connections[user_id] = {"conn": conn, "deviceType": device_type}

        # Esperar hasta que se reciba otra conexión para vincular
        while True:
            if "linkedUserId" in user_data:
                linked_user_id = user_data["linkedUserId"]
                if linked_user_id in connections:
                    linked_conn = connections[linked_user_id]["conn"]
                    link_device(user_id, linked_user_id)
                    link_device(linked_user_id, user_id)
                    linked_conn.send(f"Dispositivo {user_id} vinculado.".encode())
                    conn.send(f"Dispositivo {linked_user_id} vinculado.".encode())
                    break
    conn.close()


# Función para iniciar el servidor socket
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ip_address = socket.gethostbyname(socket.gethostname())
    port = 5051  # Debe coincidir con el puerto usado en el QR
    server_socket.bind((ip_address, port))
    server_socket.listen(5)
    print(f"Servidor iniciado en {ip_address}:{port}")

    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    start_server()
