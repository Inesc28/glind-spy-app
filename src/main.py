import flet as ft
from views.login_view import login_view


def main(page: ft.Page):
   page.title = "Glind"
   page.vertical_alignment = ft.MainAxisAlignment.CENTER 
   
   login_view(page)

ft.app(target=main, view=ft.AppView.WEB_BROWSER)
