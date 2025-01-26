import flet as ft
from views.home_view import home_view
from assets.styles import global_styles
from backend.users import validate_user


def login_view(page: ft.Page):

    page.window.always_on_top = True
    page.decoration = ft.BoxDecoration(
        image=ft.DecorationImage(
            src="https://img.freepik.com/premium-photo/abstract-black-background-copy-space_1019279-207.jpg",
            fit=ft.ImageFit.COVER,
            opacity=0.3,
        )
    )

    page.vertical_alignment = page.horizontal_alignment = "center"

    title = ft.Text("Iniciar Sesión", style=global_styles.text_styled())
    user = ft.TextField(
        label="Username", multiline=False, border_color="pink", border_radius=15
    )
    password = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
        border_color="pink",
        border_radius=15,
    )
    save_button = ft.ElevatedButton(
        text="Iniciar Sesión",
        on_click=lambda e: credentials_access(e),
        style=global_styles.button_styled(),
    )

    login_main = ft.Column(
        controls=[title, user, password, save_button],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
    )

    page.add(ft.Container(content=login_main, padding=0, margin=0, expand=False))

    def credentials_access(e):
        if validate_user(user.value, password.value):
            handle_login(page)
        else:
            ft.AlertDialog(title=ft.Text("Ha ocurrido un error"))
            

def handle_login(page: ft.Page):
    page.clean()
    home_view(page)
    page.update()

