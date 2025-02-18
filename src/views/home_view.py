import flet as ft
from assets.styles import global_styles
from views.vinc_list import vinc_list
from backend.users import connect_to_server, get_user_data, users
from backend.qr_utils import generate_and_show_qr, scan_and_connect


def home_view(page: ft.Page, logged_in_user_id: str):

    # Iniciar la conexión al servidor
    connect_to_server(logged_in_user_id, page)

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

    generate_qr_button = ft.ElevatedButton(
        text="Generar y Mostrar QR",
        on_click=lambda e: generate_and_show_qr(
            e, page, logged_in_user_id, form_connect
        ),
    )

    link_device_button = ft.ElevatedButton(
        text="Escanear QR y Conectar",
        on_click=lambda e: scan_and_connect(e, page, logged_in_user_id),
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