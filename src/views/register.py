import flet as ft
from views.login_view import login_view
from assets.styles import global_styles
from backend.users import save_data


def register(page: ft.Page):

    def register_data(e):
        save_data(email.value, user.value, password.value)

    logo = ft.Image(
        src="src/assets/img/Logo.png", fit=ft.ImageFit.COVER, width=100, height=150
    )

    logo = ft.Image(
        src="src/assets/img/Logo.png", fit=ft.ImageFit.COVER, width=100, height=150
    )

    page.window.always_on_top = True
    page.decoration = ft.BoxDecoration(
        image=ft.DecorationImage(
            src="https://img.freepik.com/premium-photo/abstract-black-background-copy-space_1019279-207.jpg",
            fit=ft.ImageFit.COVER,
            opacity=0.3,
        )
    )

    page.vertical_alignment = page.horizontal_alignment = "center"

    title = ft.Text("Regístrate", style=global_styles.text_styled())
    email = ft.TextField(
        label="Email", multiline=False, border_color="pink", border_radius=15
    )
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
        text="Registrar",
        on_click=register_data,
        style=global_styles.button_styled(),
    )
    log = ft.TextButton(
        "Si ya tienes una cuenta, Inicia Sesion",
        on_click=lambda e: handle_register(page),
    )

    register_main = ft.Column(
        controls=[logo, title, email, user, password, save_button, log],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
    )

    page.add(ft.Container(content=register_main, padding=0, margin=0, expand=False))


def handle_register(page: ft.Page):
    page.clean()
    login_view(page)
    page.update()
