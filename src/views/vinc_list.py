import flet as ft
from backend.users import users


def vinc_list(page: ft.Page, user_id, users):

    user_data = users[user_id]
    page.title = f"Dispositivos vinculados de {user_data['user']}"
    linked_devices = user_data.get("linked_devices", [])

    def reload_home(e):
        from views.home_view import home_view

        page.clean()
        home_view(page, user_id)
        page.update()

    back_button = ft.ElevatedButton(
        text="Regresar",
        on_click=reload_home,
    )

    def desvincular(e, device_id):
        # Remover el dispositivo de la lista de dispositivos vinculados
        if device_id in users[user_id]["linked_devices"]:
            users[user_id]["linked_devices"].remove(device_id)
            print(f"Dispositivo {device_id} desvinculado.")
            # Actualizar la vista
            vinc_list(page, user_id, users)
        else:
            print(f"El dispositivo {device_id} no está vinculado.")

    def visualizar(e, device_id):
        print(f"Visualizando pantalla del dispositivo {device_id}.")

    items = [
        ft.ListTile(
            title=ft.Text(f"Dispositivo: {ld}"),
            trailing=ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(
                        text="Desvincular", on_click=lambda e, ld=ld: desvincular(e, ld)
                    ),
                    ft.PopupMenuItem(
                        text="Visualizar pantalla",
                        on_click=lambda e, ld=ld: visualizar(e, ld),
                    ),
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