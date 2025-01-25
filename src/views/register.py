import flet as ft
from views.login_view import login_view
from assets.styles import global_styles

def register(page: ft.Page):

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
    email = ft.TextField(label="Email", multiline=False)
    user = ft.TextField(label="Username", multiline=False)
    password = ft.TextField(label="Password", password=True, can_reveal_password=True)
    save_button = ft.ElevatedButton(text="Registrar", on_click=lambda e: handle_register(page), style=global_styles.button_styled())
    log = ft.TextButton("Si ya tienes una cuenta, Inicia Sesion", on_click=lambda e: handle_register(page))


    register_main = ft.Column(
        controls=[
            title,
            email,
            user,
            password,
            save_button,
            log
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )

    page.add(
        ft.Container(
          content=register_main,
          padding=0,
          margin=0,
          expand=False
        )
    )
    
def handle_register(page: ft.Page):
    page.clean()
    login_view(page)
    page.update()
