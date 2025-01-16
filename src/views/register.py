import flet as ft
from views.login_view import login_view
from assets.styles import global_styles

def register(page: ft.Page):
    
    page.vertical_alignment = page.horizontal_alignment = "center"
    
    email = ft.TextField(label="Email", multiline=False)
    user = ft.TextField(label="Username", multiline=False)
    password = ft.TextField(label="Password", password=True, can_reveal_password=True)
    save_button = ft.ElevatedButton(text="Registrar", on_click=lambda e: handle_register(page), style=global_styles.button_styled())
    log = ft.TextButton("Si ya tienes una cuenta, Inicia Sesion", on_click=lambda e: handle_register(page))


    page.add(email)
    page.add(user)
    page.add(password)
    page.add(save_button)
    page.add(log)
    page.update()

    
def handle_register(page: ft.Page):
    page.clean()
    login_view(page)
    page.update()
