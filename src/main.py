import flet as ft
import asyncio
from backend.async_server import start_async_server
from views.register import register

def main(page: ft.Page):
    page.title = "Glind"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor = ft.Colors.TRANSPARENT
    # Iniciar el servidor asíncrono
    asyncio.create_task(start_async_server())
    register(page)


ft.app(target=main, view=ft.AppView.FLET_APP)
