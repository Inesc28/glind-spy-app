import socket
import threading
import json
from backend.users import link_device
from backend.server_app import connections

# Función para manejar la conexión de cada cliente
def handle_client(conn, addr):
    print(f"Conexión establecida desde {addr}")
    data = conn.recv(1024).decode()
    if data:
        userData = json.loads(data)
        userId = userData["userId"]
        deviceType = userData["deviceType"]

        # Almacenar la conexión del cliente
        connections[userId] = {"conn": conn, "deviceType": deviceType}

        # Esperar hasta que se reciba otra conexión para vincular
        while True:
            if "linkedUserId" in userData:
                linkedUserId = userData["linkedUserId"]
                if linkedUserId in connections:
                    linkedConn = connections[linkedUserId]["conn"]
                    link_device(userId, linkedUserId)
                    link_device(linkedUserId, userId)
                    linkedConn.send(f"Dispositivo {userId} vinculado.".encode())
                    conn.send(f"Dispositivo {linkedUserId} vinculado.".encode())
                    break
    conn.close()


# Función para conectar al servidor central después de escanear el código QR
def connect_to_server(qr_data, current_user_id, device_type, linked_user_id=None):
    connectionData = json.loads(qr_data)
    ipAddress = connectionData["ip"]
    port = connectionData["port"]
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((ipAddress, port))
    print(f"Conectado al servidor en {ipAddress}:{port}")

    # Enviar el userId y tipo de dispositivo actual al servidor
    userData = {
        "userId": current_user_id,
        "deviceType": device_type,
        "linkedUserId": linked_user_id,
    }
    clientSocket.send(json.dumps(userData).encode())
    clientSocket.close()
