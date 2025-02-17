import flet as ft
from backend.users import users


def vinc_list(page: ft.Page, user_id, users):

    user_data = users[user_id]
    page.title = f"Dispositivos vinculados de {user_data['user']}"
    linked_devices = user_data.get("linked_devices", [])

    def reload_home(page: ft.Page):
        from views.home_view import home_view
        page.clean()
        home_view(page, user_id)
        page.update()

    back_button = ft.ElevatedButton(
        text="Regresar",
        on_click=lambda e: reload_home(page),
    )

    def desvincular(e):
        print("Dispositivo Vinculado")

    def visualizar(e):
        print("Visualizando Pantalla")

    items = [
        ft.ListTile(
            title=ft.Text(f"Dispositivo: {ld}"),
            trailing=ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="Desvincular", on_click=desvincular),
                    ft.PopupMenuItem(text="Visualizar pantalla", on_click=visualizar),
                ]
            ),
        )
        for ld in linked_devices
    ]

    card = ft.Card(
        content=ft.Container(
            width=500,
            content=ft.Column(
                [ft.ListTile(title=ft.Text("Dispositivos Vinculados"))] + items,
                spacing=10,
            ),
            padding=ft.padding.symmetric(vertical=10),
        )
    )

    page.clean()
    page.add(back_button)
    page.add(card)
    page.update()
