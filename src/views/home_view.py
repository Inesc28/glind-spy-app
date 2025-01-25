import flet as ft

def home_view(page: ft.Page):
   appbar = ft.AppBar(
      title=ft.Text("Glind"),
      leading=ft.Icon(ft.Icons.PHONE),
      bgcolor=ft.Colors.TRANSPARENT,
      actions=[
           ft.IconButton(ft.Icons.SETTINGS, on_click=lambda _: print("Abrir configuraciones...")),
      ]
      
   )

   main_home = ft.Row(
      controls=[
         ft.TextField(label="Introduzca la Direccion", multiline=False, autofocus=True),
         ft.IconButton(ft.Icons.SEARCH)
      ],
      spacing=10,
      alignment=ft.MainAxisAlignment.CENTER,
      expand=True
   )

   main_contain = ft.Container(
      content=main_home,
      expand=True,
      alignment=ft.alignment.top_center,
      padding=10
   )

   
   page.add(appbar)
   page.add(main_contain)