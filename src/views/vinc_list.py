import flet as ft
from backend.users import users

def vinc_list(page: ft.Page, user_id, users):
    user_data = users[user_id]
    page.title = f"Dispositivos vinculados de {user_data['user']}"
    linked_devices = user_data.get('linked_devices', [])
    items = [ft.ListTile(title=ft.Text(f"Dispositivo: {ld}")) for ld in linked_devices]
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
    page.add(card)
    page.update()



    



