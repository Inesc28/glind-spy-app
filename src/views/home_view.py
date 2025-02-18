import flet as ft
import cv2
import base64
import json
import socket
import threading
from assets.styles import global_styles
from pyzbar.pyzbar import decode
from views.vinc_list import vinc_list
from backend.users import generate_qr, get_user_data, link_device, users

def home_view(page: ft.Page, logged_in_user_id: str):

    # Conectar al servidor al iniciar la vista
    def connect_to_server():
        try:
            server_ip = '127.0.0.1'  # Reemplaza con la IP del servidor si es necesario
            server_port = 5051  # Puerto del servidor
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((server_ip, server_port))
            print(f"Conectado al servidor en {server_ip}:{server_port}")

            # Enviar el user_id al servidor
            user_data = {
                "userId": logged_in_user_id,
                "deviceType": "monitored"  # Tipo de dispositivo: monitoreado
            }
            client_socket.send(json.dumps(user_data).encode())

            # Crear un hilo para manejar mensajes entrantes
            threading.Thread(target=handle_server_messages, args=(client_socket,)).start()

        except Exception as ex:
            print(f"Error al conectar al servidor: {ex}")

    # Función para manejar mensajes entrantes del servidor
    def handle_server_messages(client_socket):
        try:
            while True:
                data = client_socket.recv(1024).decode()
                if not data:
                    break
                message = json.loads(data)
                if message.get("action") == "monitor_request":
                    requester_id = message.get("requesterId")
                    # Mostrar diálogo para aceptar o denegar el monitoreo
                    show_monitor_request_dialog(requester_id, client_socket)
        except Exception as ex:
            print(f"Error en handle_server_messages: {ex}")
        finally:
            client_socket.close()

    # Función para mostrar el diálogo de solicitud de monitoreo
    def show_monitor_request_dialog(requester_id, client_socket):
        def accept_monitoring(e):
            response = {"action": "monitor_response", "accepted": True, "userId": logged_in_user_id}
            client_socket.send(json.dumps(response).encode())
            page.dialog.open = False
            page.update()

        def deny_monitoring(e):
            response = {"action": "monitor_response", "accepted": False, "userId": logged_in_user_id}
            client_socket.send(json.dumps(response).encode())
            page.dialog.open = False
            page.update()

        content = ft.Column(
            [
                ft.Text(f"El usuario {requester_id} quiere monitorear su dispositivo."),
                ft.Row(
                    [
                        ft.ElevatedButton("Aceptar", on_click=accept_monitoring),
                        ft.ElevatedButton("Denegar", on_click=deny_monitoring),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            spacing=20,
        )
        page.dialog = ft.AlertDialog(
            title=ft.Text("Solicitud de Monitoreo"),
            content=content,
            modal=True,
            on_dismiss=lambda e: None,
        )
        page.dialog.open = True
        page.update()

    # Iniciar la conexión al servidor
    connect_to_server()

    def list_in(e):
        vinc_list(page, logged_in_user_id, users)
        page.update()

    user_info = get_user_data(logged_in_user_id)

    if user_info:
        user_code = ft.Text(value=f"{user_info['id']}")
        user_name = ft.Text(
            value=f"{user_info['user']}", style=global_styles.global_text()
        )

    logo = ft.Image(
        src="URL_DEL_LOGO",  # Reemplaza con la URL de tu logo
        fit=ft.ImageFit.COVER,
        width=100,
        height=120,
    )

    appbar = ft.AppBar(
        leading=ft.Container(content=logo),
        title=ft.Text("Glind", style=global_styles.global_text()),
        bgcolor=ft.Colors.BLACK12,
        actions=[
            ft.IconButton(
                icon=ft.Icons.SETTINGS,
                on_click=lambda _: print("Abrir configuraciones...")
            )
        ],
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
                ft.IconButton(icon=ft.Icons.HOME_FILLED, data="1", icon_color="white"),
                ft.IconButton(
                    icon=ft.Icons.LIST_ALT_ROUNDED,
                    data="2",
                    icon_color="white",
                    on_click=list_in,
                ),
            ],
        ),
    )

    form_connect = ft.Column(
        controls=[user_name, user_code],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
    )

    def generate_and_show_qr(e):
        try:
            print("Botón 'Generar y Mostrar QR' presionado")

            # Eliminar cualquier QR preexistente
            if hasattr(page, 'qr_container'):
                form_connect.controls.remove(page.qr_container)

            # Generar QR y verificar si devuelve datos
            qr_image_data = generate_qr(logged_in_user_id)
            if qr_image_data:
                print("Datos del QR generados.")

                # Verificar si base64 encoding está funcionando correctamente
                qr_base64 = base64.b64encode(qr_image_data).decode('utf-8')
                print("Datos del QR en base64 generados.")

                # Creación de la imagen QR
                qr_image = ft.Image(src_base64=qr_base64, width=200, height=200)

                # Crear un contenedor con animación de opacidad
                page.qr_container = ft.Container(
                    content=qr_image,
                    opacity=0.0,
                    animate_opacity=500  # duración de la animación en milisegundos
                )

                # Agregar el contenedor al formulario
                form_connect.controls.append(page.qr_container)
                page.update()

                # Iniciar la animación cambiando la opacidad
                page.qr_container.opacity = 1.0
                page.update()

                print("Imagen QR añadida y animación de opacidad iniciada.")
            else:
                print("No se pudo generar el código QR")
        except Exception as ex:
            print(f"Error en generate_and_show_qr: {ex}")

    def scan_and_connect(e):
        try:
            print("Botón 'Escanear QR y Conectar' presionado")
            qr_data = None

            # Crear una imagen en la interfaz de Flet para mostrar el video
            video_image = ft.Image()
            page.overlay.append(video_image)
            page.update()

            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                print("No se pudo abrir la cámara")
                page.dialog = ft.AlertDialog(
                    title=ft.Text("Error"),
                    content=ft.Text("No se pudo abrir la cámara.")
                )
                page.dialog.open = True
                page.update()
                return

            while True:
                ret, frame = cap.read()
                if not ret:
                    print("No se pudo recibir el fotograma")
                    break

                # Convertir el fotograma a formato compatible con Flet
                _, buffer = cv2.imencode('.jpg', frame)
                img_bytes = buffer.tobytes()
                video_image.src_base64 = base64.b64encode(img_bytes).decode('utf-8')
                page.update()

                # Intentar decodificar códigos QR
                decoded_objs = decode(frame)
                if decoded_objs:
                    qr_data = decoded_objs[0].data.decode('utf-8')
                    print("QR detectado:", qr_data)
                    break

            # Liberar recursos y limpiar la interfaz
            cap.release()
            video_image.src_base64 = None
            page.overlay.remove(video_image)
            page.update()

            if qr_data:
                # Intentar cargar los datos del QR como un diccionario JSON
                try:
                    connection_data = json.loads(qr_data)
                    # Verificar si el diccionario tiene las claves esperadas
                    required_keys = {"userId", "ip", "port"}
                    if required_keys.issubset(connection_data.keys()):
                        target_user_id = connection_data["userId"]
                        linked_devices = users[logged_in_user_id].get("linked_devices", [])

                        if target_user_id == logged_in_user_id:
                            page.dialog = ft.AlertDialog(
                                title=ft.Text("Error"),
                                content=ft.Text("No puedes vincular tu propio dispositivo.")
                            )
                            page.dialog.open = True
                            page.update()
                        elif target_user_id in linked_devices:
                            page.dialog = ft.AlertDialog(
                                title=ft.Text("Información"),
                                content=ft.Text("Este dispositivo ya está vinculado.")
                            )
                            page.dialog.open = True
                            page.update()
                            print(f"El dispositivo {target_user_id} ya está vinculado.")
                        else:
                            # Conectarse al servidor y enviar solicitud de monitoreo
                            server_ip = '127.0.0.1'  # Reemplaza con la IP del servidor
                            server_port = 5051
                            monitor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            monitor_socket.connect((server_ip, server_port))
                            print(f"Conectado al servidor en {server_ip}:{server_port}")

                            # Enviar el userId al servidor
                            user_data = {
                                "userId": logged_in_user_id,
                                "deviceType": "monitor"  # Dispositivo monitor
                            }
                            monitor_socket.send(json.dumps(user_data).encode())

                            # Enviar solicitud de monitoreo
                            monitor_request = {
                                "action": "monitor_request",
                                "targetUserId": target_user_id,
                                "requesterId": logged_in_user_id
                            }
                            monitor_socket.send(json.dumps(monitor_request).encode())

                            # Esperar respuesta del servidor
                            response_data = monitor_socket.recv(1024).decode()
                            response = json.loads(response_data)
                            if response.get("action") == "monitor_response":
                                accepted = response.get("accepted")
                                if accepted:
                                    # Agregar el dispositivo a la lista vinculada
                                    link_device(logged_in_user_id, target_user_id)
                                    print(f"Dispositivos vinculados: {logged_in_user_id} <--> {target_user_id}")
                                    page.dialog = ft.AlertDialog(
                                        title=ft.Text("Éxito"),
                                        content=ft.Text("El usuario ha aceptado el monitoreo. Dispositivo vinculado exitosamente.")
                                    )
                                else:
                                    page.dialog = ft.AlertDialog(
                                        title=ft.Text("Información"),
                                        content=ft.Text("El usuario ha denegado el monitoreo.")
                                    )
                                page.dialog.open = True
                                page.update()

                            monitor_socket.close()
                    else:
                        print("El QR no contiene los datos necesarios.")
                        page.dialog = ft.AlertDialog(
                            title=ft.Text("Error"),
                            content=ft.Text("El código QR escaneado no es válido para este escaneo.")
                        )
                        page.dialog.open = True
                        page.update()
                except json.JSONDecodeError:
                    print("El QR no es un JSON válido.")
                    page.dialog = ft.AlertDialog(
                        title=ft.Text("Error"),
                        content=ft.Text("El código QR escaneado no es válido para este escaneo.")
                    )
                    page.dialog.open = True
                    page.update()
            else:
                page.dialog = ft.AlertDialog(
                    title=ft.Text("Error"),
                    content=ft.Text("No se pudo escanear el código QR.")
                )
                page.dialog.open = True
                page.update()
        except Exception as ex:
            print(f"Error en scan_and_connect: {ex}")

    generate_qr_button = ft.ElevatedButton(
        text="Generar y Mostrar QR",
        on_click=generate_and_show_qr,
    )

    link_device_button = ft.ElevatedButton(
        text="Escanear QR y Conectar",
        on_click=scan_and_connect,
    )

    form_connect.controls.append(generate_qr_button)
    form_connect.controls.append(link_device_button)

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
            controls=[nav],
            width=page.width,
            height=page.height,
            alignment=ft.alignment.center,
        )
    )

    page.update()