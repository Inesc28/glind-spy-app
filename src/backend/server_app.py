import socket
import threading
import json

users = {}

# Función para manejar la conexión de cada cliente
def handle_client(conn, addr):
    try:
        print(f"Conexión establecida desde {addr}")
        data = conn.recv(1024).decode()
        if data:
            user_data = json.loads(data)
            user_id = user_data["userId"]

            # Registrar la conexión del usuario
            users[user_id] = {"conn": conn, "addr": addr}
            print(f"Usuario {user_id} conectado al servidor.")

            while True:
                data = conn.recv(1024)
                if not data:
                    break

        # Eliminar al usuario de la lista al desconectarse
        print(f"Usuario {user_id} desconectado del servidor.")
        if user_id in users:
            del users[user_id]

    except Exception as ex:
        print(f"Error en handle_client: {ex}")
    finally:
        conn.close()


# Función para iniciar el servidor socket
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip_address = "0.0.0.0"
    port = 5051
    server_socket.bind((ip_address, port))
    server_socket.listen(5)
    print(f"Servidor iniciado en {ip_address}:{port}")

    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    start_server()