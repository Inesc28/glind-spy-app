import socket
import time
import pickle
import numpy as np
import mss

# Crear un socket de servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 54321))
server_socket.listen(1)

print("Servidor escuchando en el puerto 54321...")

try:
    # Aceptar una conexión
    client_socket, client_address = server_socket.accept()
    print(f"Conexión aceptada de {client_address}")

    with mss.mss() as sct:
        while True:
            try:
                # Capturar la pantalla
                screenshot = sct.grab(sct.monitors[1])
                screenshot_np = np.array(screenshot)

                # Serializar la imagen
                data = pickle.dumps(screenshot_np)

                # Enviar el tamaño de los datos
                client_socket.sendall(len(data).to_bytes(4, byteorder='big'))

                # Enviar los datos
                client_socket.sendall(data)
            except socket.error as e:
                print(f"Error al enviar los datos: {e}")
                break

            # Esperar un poco antes de capturar de nuevo (para no saturar la red)
            time.sleep(0.1)

except socket.error as e:
    print(f"Error de conexión: {e}")

finally:
    client_socket.close()
    server_socket.close()
