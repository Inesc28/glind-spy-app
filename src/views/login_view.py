import flet as ft
from views.home_view import home_view
from assets.styles import global_styles

def login_view(page: ft.Page):
    
    page.vertical_alignment = page.horizontal_alignment = "center"

    user = ft.TextField(label="Username", multiline=False)
    password = ft.TextField(label="Password", password=True, can_reveal_password=True)
    save_button = ft.ElevatedButton(text="Login", on_click=lambda e: handle_login(page), style=global_styles.button_styled())

    page.add(user)
    page.add(password)
    page.add(save_button)
    page.update()

    
def handle_login(page: ft.Page):
    page.clean()
    home_view(page)
    page.update()
