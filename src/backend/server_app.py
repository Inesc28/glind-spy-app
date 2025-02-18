import socket
import threading
import json

users = {}  # Diccionario de usuarios conectados

# Función para manejar la conexión de cada cliente
def handle_client(conn, addr):
    try:
        print(f"Conexión establecida desde {addr}")
        data = conn.recv(1024).decode()
        if data:
            user_data = json.loads(data)
            user_id = user_data["userId"]
            device_type = user_data.get("deviceType")

            # Registrar la conexión del usuario
            users[user_id] = {"conn": conn, "deviceType": device_type, "addr": addr}
            print(f"Usuario {user_id} conectado al servidor.")

            # Mantener la conexión abierta para recibir mensajes
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break
                message = json.loads(data)

                if message.get("action") == "monitor_request":
                    target_user_id = message.get("targetUserId")
                    requester_id = message.get("requesterId")

                    # Verificar si el usuario objetivo está en línea
                    if target_user_id in users:
                        target_conn = users[target_user_id]["conn"]
                        # Enviar solicitud al usuario objetivo
                        monitor_request = {
                            "action": "monitor_request",
                            "requesterId": requester_id,
                        }
                        target_conn.send(json.dumps(monitor_request).encode())
                    else:
                        # Enviar respuesta de que el usuario no está en línea
                        response = {
                            "action": "monitor_response",
                            "accepted": False,
                            "message": f"El usuario {target_user_id} no está en línea.",
                        }
                        conn.send(json.dumps(response).encode())

                elif message.get("action") == "monitor_response":
                    accepted = message.get("accepted")
                    user_id_response = message.get("userId")
                    # Enviar respuesta al usuario que solicitó el monitoreo
                    requester_conn = users.get(user_id_response, {}).get("conn")
                    if requester_conn:
                        response = {
                            "action": "monitor_response",
                            "accepted": accepted,
                            "userId": user_id,  # userId del usuario que respondió
                        }
                        requester_conn.send(json.dumps(response).encode())

        # Eliminar al usuario de la lista al desconectarse
        print(f"Usuario {user_id} desconectado del servidor.")
        del users[user_id]

    except Exception as ex:
        print(f"Error en handle_client: {ex}")
    finally:
        conn.close()


# Función para iniciar el servidor socket
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip_address = "0.0.0.0"  # Escuchar en todas las interfaces
    port = 5051  # Puerto del servidor
    server_socket.bind((ip_address, port))
    server_socket.listen(5)
    print(f"Servidor iniciado en {ip_address}:{port}")

    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    start_server()