import flet as ft
import base64
from backend.users import generate_qr, get_user_data
from assets.styles import global_styles
from views.vinc_list import vinc_list

def home_view(page: ft.Page, logged_in_user_id: str):
    user_info = get_user_data(logged_in_user_id)

    if user_info:
        user_code = ft.Text(value=f"{user_info['id']}")
        user_name = ft.Text(
            value=f"{user_info['user']}", style=global_styles.global_text()
        )

    logo = ft.Image(
        src="URL_DEL_LOGO",
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
                on_click=lambda _: print("Abrir configuraciones..."),
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
                ft.IconButton(
                    icon=ft.Icons.HOME_FILLED, data="1", icon_color="white"
                ),  
                ft.IconButton(
                    icon=ft.Icons.LIST_ALT_ROUNDED,
                    data="2",
                    icon_color="white", 
                    on_click=vinc_list,
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

            # Generar QR y verificar si devuelve datos
            qr_image_data = generate_qr(logged_in_user_id)
            if qr_image_data:
                print("Datos del QR generados:", qr_image_data)

                # Verificar si base64 encoding está funcionando correctamente
                qr_base64 = base64.b64encode(qr_image_data).decode("utf-8")
                print("Datos del QR en base64:", qr_base64)

                # Verificar la configuración de la imagen
                qr_image = ft.Image(src_base64=qr_base64, width=200, height=200)
                print("Imagen QR configurada.")

                # Añadir la imagen a la página y actualizar
                form_connect.controls.append(qr_image)
                page.update()
                print("Imagen QR añadida y página actualizada.")
            else:
                print("No se pudo generar el código QR")
        except Exception as ex:
            print(f"Error en generate_and_show_qr: {ex}")


    generate_qr_button = ft.ElevatedButton(
        text="Generar y Mostrar QR", on_click=generate_and_show_qr
    )

    link_device_button = ft.ElevatedButton(
        text="Escanear QR y Conectar"
    )

    form_connect.controls.append(generate_qr_button)
    form_connect.controls.append(link_device_button)

    page.add(appbar)
    page.add(ft.Container(content=form_connect, padding=0, margin=0, expand=False))
    page.add(
        ft.Stack(
            controls=[nav],
            width=page.width,
            height=page.height,
            alignment=ft.alignment.center,
        )
    )

    page.update()