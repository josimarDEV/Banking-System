# Home Page
import flet as ft
from flet import *
from flet_route import Params, Basket


LIGHT_SEED_COLOR = colors.DEEP_ORANGE
DARK_SEED_COLOR = colors.INDIGO


def home(page: ft.Page, params= Params, basket=Basket):
    # Adiciona controle de update na página
    def check_item_clicked(e):
        e.control.checked = not e.control.checked
        page.update()
    page.title = "Banco Silva"
    page.theme_mode = "dark"
    page.window_resizable = False
    page.window_width = 900
    page.window_height = 920
    page.horizontal_alignment = MainAxisAlignment.CENTER
    page.theme = Theme(color_scheme_seed=LIGHT_SEED_COLOR, use_material3=True)
    page.dark_theme = Theme(color_scheme_seed=DARK_SEED_COLOR, use_material3=True)
    page.scroll = True
    def check_item_clicked(e):
        e.control.checked = not e.control.checked
        page.update()
    

    def toggle_theme_mode(e):
        page.theme_mode = "dark" if page.theme_mode == "light" else "light"
        lightMode.icon = (
            icons.LIGHT_MODE_ROUNDED if page.theme_mode == "light" else icons.DARK_MODE_ROUNDED
        )
        page.update()

    lightMode = IconButton(
        icons.LIGHT_MODE_ROUNDED if page.theme_mode == "light" else icons.DARK_MODE_ROUNDED,
        on_click=toggle_theme_mode,
    )
    
    page.padding = 50

    welcome = Container(
        content=Row(
            [
                Text(
                    'SEJA BEM VINDO',
                    size=80,
                    weight='bold',
                    color=colors.YELLOW_900
                )
            ],
            alignment=MainAxisAlignment.CENTER,
        ),
        top=100, left=100,
        visible=True,
    )
    
    welcome_textfield = ft.Container(
        content=Row(
            [
                IconButton(
                    icon=icons.LOGIN,
                    icon_color=colors.YELLOW_900,
                    icon_size=200,
                    on_click=lambda _: page.go("/login")
                ),
            ],
            alignment=MainAxisAlignment.CENTER,
        ),
        top=600, right=360
        )
    
    interface_appbar = AppBar(
        toolbar_height=50,
        bgcolor=colors.SECONDARY_CONTAINER,
        leading=Icon(icons.ACCOUNT_BALANCE_ROUNDED),
        leading_width=40,
        title=Text("BANCO SILVA", weight='bold', size=25),
        center_title=True,
        actions=[
            PopupMenuButton(
                lightMode,
                tooltip='TEMA'
                )
        ]
    )
    
    return View(
        "/home",
        controls= [
            interface_appbar, Stack([welcome_textfield, welcome], height=920)
        ]
    )