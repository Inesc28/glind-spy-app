import flet as ft
from assets.styles import global_styles
from backend.users import connect_to_server_threaded, get_user_data, get_connected_users


def home_view(page: ft.Page, logged_in_user_id: str):

    # Iniciar la conexión al servidor en un hilo separado
    connect_to_server_threaded(logged_in_user_id, page)

    # Función para refrescar la interfaz
    def refresh_ui(e=None):
        user_info = get_user_data(logged_in_user_id)

        # Limpiar los controles actuales
        page.controls.clear()

        # Verificar si se obtuvo correctamente la información del usuario
        if user_info:
            user_code = ft.Text(value=f"ID: {user_info['id']}")
            user_name = ft.Text(
                value=f"Usuario: {user_info['user']}", style=global_styles.global_text()
            )
        else:
            user_code = ft.Text(value="ID desconocido")
            user_name = ft.Text(
                value="Usuario desconocido", style=global_styles.global_text()
            )

        # Crear el logo
        logo = ft.Image(
            src="URL_DEL_LOGO",  # Reemplaza con la URL de tu logo
            fit=ft.ImageFit.COVER,
            width=100,
            height=120,
        )

        # Crear el AppBar y asignarlo a la página
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
        page.appbar = appbar  # Asignar el AppBar a la página

        # Botón para actualizar la lista de usuarios conectados
        refresh_button = ft.ElevatedButton(
            text="Actualizar Lista",
            icon=ft.Icons.REFRESH,
            on_click=refresh_ui,
        )

        # Obtener usuarios conectados del servidor
        connected_users_list = get_connected_users(logged_in_user_id)

        # Crear listado de usuarios conectados
        items = []
        for user in connected_users_list:
            user_id = user.get("userId")
            username = user.get("username")
            if user_id != logged_in_user_id:
                item = ft.ListTile(
                    title=ft.Text(f"Usuario: {username}"),
                    trailing=ft.PopupMenuButton(
                        items=[
                            ft.PopupMenuItem(
                                text="Desvincular",
                                on_click=lambda e, user_id=user_id: desvincular(
                                    e, user_id
                                ),
                            ),
                            ft.PopupMenuItem(
                                text="Visualizar pantalla",
                                on_click=lambda e, user_id=user_id: visualizar(
                                    e, user_id
                                ),
                            ),
                        ]
                    ),
                )
                items.append(item)

        # Funciones para desvincular y visualizar usuarios
        def desvincular(e, user_id):
            print(f"Usuario {user_id} desvinculado.")
            # Aquí puedes agregar la lógica para desvincular al usuario

        def visualizar(e, user_id):
            print(f"Visualizando pantalla del usuario {user_id}.")
            # Aquí puedes agregar la lógica para visualizar la pantalla del usuario

        # Crear la tarjeta con el listado de usuarios conectados
        card = ft.Card(
            content=ft.Container(
                width=500,
                content=ft.Column(
                    [ft.ListTile(title=ft.Text("Usuarios Conectados"))] + items,
                    spacing=10,
                ),
                padding=ft.padding.symmetric(vertical=10),
            )
        )

        # Información del usuario y botón de actualización
        form_connect = ft.Column(
            controls=[user_name, user_code, refresh_button],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )

        # Agregar controles a la página
        page.controls.extend(
            [
                ft.Container(content=form_connect, padding=0, margin=0, expand=False),
                card,
            ]
        )

        # Actualizar la página
        page.update()

    # Realizar la primera actualización de la interfaz
    refresh_ui()