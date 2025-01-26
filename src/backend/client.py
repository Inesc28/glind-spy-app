import socket
import pickle
import base64
import io
import flet as ft
from PIL import Image



def client(page: ft.Page):

    def connect(e):

        # Iniciar conexión con el servidor
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("localhost", 54321))

        # Crear un control de imagen vacío
        img = ft.Image(width=300, height=600)
        page.add(img)

        try:
            while True:
                # Recibir el tamaño de los datos
                try:
                    data_size = int.from_bytes(client_socket.recv(4), byteorder="big")
                except socket.error as e:
                    print(f"Error al recibir el tamaño de los datos: {e}")
                    break

                # Recibir los datos
                data = b""
                while len(data) < data_size:
                    try:
                        packet = client_socket.recv(data_size - len(data))
                        if not packet:
                            break
                        data += packet
                    except socket.error as e:
                        print(f"Error al recibir los datos: {e}")
                        break

                # Deserializar la imagen
                screenshot_np = pickle.loads(data)
                screenshot = Image.fromarray(screenshot_np)

                # Convertir la imagen a base64 para Flet
                img_bytes = io.BytesIO()
                screenshot.save(img_bytes, format="PNG")
                img_bytes.seek(0)
                img_base64 = base64.b64encode(img_bytes.read()).decode("utf-8")

                # Actualizar la imagen en la pantalla del cliente
                img.src_base64 = img_base64
                page.update()

        except socket.error as e:
            print(f"Error de conexión: {e}")

        finally:
            client_socket.close()
