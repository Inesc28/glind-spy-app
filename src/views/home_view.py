import flet as ft
from assets.styles import global_styles
from backend.users import connect_to_server_threaded, get_user_data, users


def home_view(page: ft.Page, logged_in_user_id: str):

    # Iniciar la conexión al servidor en un hilo separado
    connect_to_server_threaded(logged_in_user_id, page)

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
                    on_click=None,  # Botón deshabilitado
                    disabled=True,  # Añadir propiedad disabled
                ),
            ],
        ),
    )

    form_connect = ft.Column(
        controls=[user_name, user_code],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
    )

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