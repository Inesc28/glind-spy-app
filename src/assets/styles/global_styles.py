import flet as ft

def button_styled():
    return ft.ButtonStyle(
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.RED,
        shape=ft.RoundedRectangleBorder(radius=10),
        padding=50
    )
