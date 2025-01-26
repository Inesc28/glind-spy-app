import flet as ft

def button_styled():
    return ft.ButtonStyle(
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.PINK,
        shape=ft.RoundedRectangleBorder(radius=10),
    )

def text_styled():
    return ft.TextStyle(
        color=ft.Colors.WHITE,
        size=20
    )
