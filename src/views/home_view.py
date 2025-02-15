import flet as ft
import base64
from backend.users import generate_qr, get_user_data
from assets.styles import global_styles
from views.link_device_view import link_device_view


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
        bgcolor=ft.colors.BLACK12,
        actions=[
            ft.IconButton(
                icon=ft.icons.SETTINGS,
                on_click=lambda _: print("Abrir configuraciones..."),
            )
        ],
    )

    nav = ft.Container(
        shape=ft.BoxShape.CIRCLE,
        bgcolor=ft.colors.BLACK,
        alignment=ft.alignment.center,
        padding=0,
        height=50,
        margin=ft.margin.only(top=10),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            controls=[
                ft.IconButton(icon=ft.icons.HOME_FILLED, data="1", icon_color="white"),
                ft.IconButton(
                    icon=ft.icons.LIST_ALT_ROUNDED, data="2", icon_color="white"
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
            qr_image_data = generate_qr(logged_in_user_id)
            if qr_image_data:
                qr_base64 = base64.b64encode(qr_image_data).decode("utf-8")
                qr_image = ft.Image(src_base64=qr_base64, width=200, height=200)
                page.add(qr_image)
                page.update()
            else:
                print("No se pudo generar el código QR")
        except Exception as ex:
            print(f"Error en generate_and_show_qr: {ex}")

    def open_link_device_view(e):
        try:
            print("Botón 'Escanear QR y Conectar' presionado")
            page.views.clear()
            link_device_view(page, logged_in_user_id, "monitor")
            page.update()
        except Exception as ex:
            print(f"Error en open_link_device_view: {ex}")

    generate_qr_button = ft.ElevatedButton(
        text="Generar y Mostrar QR", on_click=generate_and_show_qr
    )

    link_device_button = ft.ElevatedButton(
        text="Escanear QR y Conectar", on_click=open_link_device_view
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