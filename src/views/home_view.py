import flet as ft
from backend.client import client
from assets.styles import global_styles

def home_view(page: ft.Page):

   appbar = ft.AppBar(
      title=ft.Text("Glind"),
      bgcolor=ft.Colors.BLACK12,
      actions=[
           ft.IconButton(ft.Icons.SETTINGS, on_click=lambda _: print("Abrir configuraciones...")),
      ]
    )

   nav = ft.Container(
        shape=ft.BoxShape.CIRCLE,
        bgcolor=ft.Colors.BLACK,
        alignment=ft.alignment.center,
        padding=0,
        height=50,
        margin=ft.margin.only(top=10),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            controls=[
                ft.IconButton(icon=ft.Icons.HOME_FILLED, data="1", icon_color="white"),
                ft.IconButton(icon=ft.Icons.LIST_ALT_ROUNDED, data="2", icon_color="white"),
            ]
        )
    )
   
   server_button = ft.ElevatedButton(text="Servidor", style=global_styles.button_styled())
   client_button = ft.ElevatedButton(text="Cliente", style=global_styles.button_styled())
   
   form_connect = ft.Row(
        controls=[
            server_button,
            client_button
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )

   page.add(appbar)
   page.add(
        ft.Container(
            content=form_connect,
            padding=0,
            margin=0,
            expand=False
        )
    )
   page.add(
        ft.Stack(
            controls=[
                nav
            ],
            width=page.width,
            height=page.height,
            alignment=ft.alignment.center
        )
    )




