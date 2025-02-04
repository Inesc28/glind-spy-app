import flet as ft
from views.login_view import login_view
from assets.styles import global_styles
from backend.users import register_new_user


def register(page: ft.Page):

    def register_data(e):
        register_new_user(email.value, user.value, password.value)

    logo = ft.Image(
        src="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/3044f73c-0547-4b01-aeec-7ebff6555e1b/dj1p9o7-af65f7df-e4ef-497f-9cb7-b4545d76045e.png/v1/fill/w_400,h_400/logo_glind_by_coloringdancingedits_dj1p9o7-fullview.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9NDAwIiwicGF0aCI6IlwvZlwvMzA0NGY3M2MtMDU0Ny00YjAxLWFlZWMtN2ViZmY2NTU1ZTFiXC9kajFwOW83LWFmNjVmN2RmLWU0ZWYtNDk3Zi05Y2I3LWI0NTQ1ZDc2MDQ1ZS5wbmciLCJ3aWR0aCI6Ijw9NDAwIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmltYWdlLm9wZXJhdGlvbnMiXX0.e7HioozPY8w7uJYU9ucOlj32A2t67eokOm5vkh3go-A",
        fit=ft.ImageFit.COVER,
        width=120,
        height=160,
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
