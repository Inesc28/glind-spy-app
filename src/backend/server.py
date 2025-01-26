import socket
from spy_utils import send_screen_capture

# Crear un socket de servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 54321))
server_socket.listen(1)

print("Servidor escuchando en el puerto 54321...")

try:
    # Aceptar una conexión
    client_socket, client_address = server_socket.accept()
    print(f"Conexión aceptada de {client_address}")
    send_screen_capture(client_socket, delay=0.1)
except socket.error as e:
    print(f"Error de conexión: {e}")
finally:
    client_socket.close()
    server_socket.close()
