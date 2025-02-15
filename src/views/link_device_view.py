import flet as ft
from backend.connection import connect_to_server
import base64

def link_device_view(page: ft.Page, current_user_id, device_type):
    qr_data_field = ft.TextField(label="Datos del QR escaneado", visible=False)

    def on_qr_scanned(e):
        connect_to_server(
            base64.b64decode(qr_data_field.value).decode(), current_user_id, device_type
        )
        ft.dialog_alert("Dispositivo vinculado exitosamente")

    scan_qr_button = ft.ElevatedButton(
        text="Escanear QR y Conectar", on_click=on_qr_scanned
    )

    page.add(
        ft.Column(
            controls=[qr_data_field, scan_qr_button],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )