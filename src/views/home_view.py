import flet as ft
import cv2
import base64
import json
from pyzbar.pyzbar import decode
from backend.users import generate_qr, get_user_data,link_device, users
from backend.client import scan_qr_code, connect_to_server
from assets.styles import global_styles
from views.vinc_list import vinc_list

def home_view(page: ft.Page, logged_in_user_id: str):

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
        src="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/3044f73c-0547-4b01-aeec-7ebff6555e1b/dj1p9o7-af65f7df-e4ef-497f-9cb7-b4545d76045e.png/v1/fill/w_400,h_400/logo_glind_by_coloringdancingedits_dj1p9o7-fullview.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9NDAwIiwicGF0aCI6IlwvZlwvMzA0NGY3M2MtMDU0Ny00YjAxLWFlZWMtN2ViZmY2NTU1ZTFiXC9kajFwOW83LWFmNjVmN2RmLWU0ZWYtNDk3Zi05Y2I3LWI0NTQ1ZDc2MDQ1ZS5wbmciLCJ3aWR0aCI6Ijw9NDAwIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmltYWdlLm9wZXJhdGlvbnMiXX0.e7HioozPY8w7uJYU9ucOlj32A2t67eokOm5vkh3go-A",
        fit=ft.ImageFit.COVER,
        width=100,
        height=120,
    )

    appbar = ft.AppBar(
        leading=ft.Container(content=logo),
        title=ft.Text("Glind", style=global_styles.global_text()),
        bgcolor=ft.Colors.BLACK12,  # Usamos ft.Colors en lugar de ft.colors
        actions=[
            ft.IconButton(
                icon=ft.Icons.SETTINGS,  # Usamos ft.Icons en lugar de ft.icons
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
                ft.IconButton(icon=ft.Icons.HOME_FILLED, data="1", icon_color="white"),  # Usamos ft.Icons en lugar de ft.icons
                ft.IconButton(
                    icon=ft.Icons.HOME_FILLED, data="1", icon_color="white"
                ),  
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
        alignment=ft.CrossAxisAlignment.CENTER,
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
                ft.AlertDialog("No se pudo abrir la cámara")
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
                        # Agregar el userId del dispositivo escaneado a la lista de dispositivos vinculados
                        link_device(logged_in_user_id, target_user_id)
                        print(f"Dispositivos vinculados: {logged_in_user_id} <--> {target_user_id}")
                        ft.AlertDialog("Dispositivo vinculado exitosamente")
                    else:
                        print("El QR no contiene los datos necesarios.")
                        ft.AlertDialog("El código QR escaneado no es válido para este escaneo.")
                except json.JSONDecodeError:
                    print("El QR no es un JSON válido.")
                    ft.AlertDialog("El código QR escaneado no es válido para este escaneo.")
            else:
                ft.AlertDialog("No se pudo escanear el código QR")
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
