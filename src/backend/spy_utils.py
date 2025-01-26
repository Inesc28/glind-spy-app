import socket
import time
import pickle
import numpy as np
import mss


def send_screen_capture(client_socket, delay=0.1):
    """
    client_socket (socket.socket): El socket del cliente conectado.
    delay (float): Tiempo de espera entre capturas, en segundos.
    """
    with mss.mss() as sct:
        while True:
            try:
                # Capturar la pantalla
                screenshot = sct.grab(sct.monitors[1])
                screenshot_np = np.array(screenshot)

                # Serializar la imagen
                data = pickle.dumps(screenshot_np)

                # Enviar el tamaño de los datos
                client_socket.sendall(len(data).to_bytes(4, byteorder="big"))

                # Enviar los datos
                client_socket.sendall(data)
            except socket.error as e:
                print(f"Error al enviar los datos: {e}")
                break

            # Esperar antes de la siguiente captura
            time.sleep(delay)
