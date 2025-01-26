import flet as ft
from views.register import register


def main(page: ft.Page):
   page.title = "Glind"
   page.vertical_alignment = ft.MainAxisAlignment.CENTER
   page.bgcolor = ft.Colors.TRANSPARENT
   register(page)

ft.app(target=main, view=ft.AppView.FLET_APP)
