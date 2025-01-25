import socket
import pickle
import flet as ft
from PIL import Image
import io
import base64

def client(page: ft.Page):

    appbar = ft.AppBar(
      title=ft.Text("Glind"),
      bgcolor=ft.Colors.BLACK12,
      actions=[
           ft.IconButton(ft.Icons.SETTINGS, on_click=lambda _: print("Abrir configuraciones...")),
      ]
    )

    nav = ft.Container(
        shape=ft.BoxShape.CIRCLE,
        bgcolor=ft.Colors.BLACK,
        alignment=ft.alignment.center,
        padding=0,
        height=50,
        margin=ft.margin.only(top=10),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            controls=[
                ft.IconButton(icon=ft.icons.HOME_FILLED, data="1", icon_color="white"),
                ft.IconButton(icon=ft.icons.LIST_ALT_ROUNDED, data="2", icon_color="white"),
            ]
        )
    )


    def connect(e):
        ip_server = ip_input.value.strip()  # Obtener y limpiar el valor ingresado en el TextField

        # Validar la dirección IP
        if not ip_server or not validate_ip(ip_server):
            page.snack_bar = ft.SnackBar(ft.Text("Por favor, ingrese una dirección IP válida."))
            page.snack_bar.open = True
            page.update()
            return

        try:
            # Iniciar conexión con el servidor
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((ip_server, 54321))

            # Crear un control de imagen vacío
            img = ft.Image(width=300, height=600)
            page.add(img)

            try:
                while True:
                    # Recibir el tamaño de los datos
                    try:
                        data_size = int.from_bytes(client_socket.recv(4), byteorder='big')
                    except socket.error as e:
                        print(f"Error al recibir el tamaño de los datos: {e}")
                        break

                    # Recibir los datos
                    data = b''
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
                    screenshot.save(img_bytes, format='PNG')
                    img_bytes.seek(0)
                    img_base64 = base64.b64encode(img_bytes.read()).decode('utf-8')

                    # Actualizar la imagen en la pantalla del cliente
                    img.src_base64 = img_base64
                    page.update()

            except socket.error as e:
                print(f"Error de conexión: {e}")

            finally:
                client_socket.close()

        except socket.gaierror as e:
            print(f"Error al resolver la dirección: {e}")

    def validate_ip(ip):
        try:
            socket.inet_aton(ip)
            return True
        except socket.error:
            return False


    ip_input = ft.TextField(label="Dirección IP del servidor")
    connect_button = ft.ElevatedButton(text="Conectar", on_click=connect)
    
    form_connect = ft.Column(
        controls=[
            ip_input,
            connect_button
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )

    # Añadir los controles a la página
    page.add(appbar)
    page.add(
        ft.Container(
            content=form_connect,
            padding=0,
            margin=0,
            expand=False
        )
    )
    page.add(
        ft.Stack(
            controls=[
                nav
            ],
            width=page.width,
            height=page.height,
            alignment=ft.alignment.center
        )
    )




