import flet as ft
from flet import *
from flet_route import Params, Basket




LIGHT_SEED_COLOR = colors.DEEP_ORANGE
DARK_SEED_COLOR = colors.INDIGO

def login(page: ft.Page, params=Params, basket=Basket):
    global login_value, password_value
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
    
    icon_login = Container(
        content=Row(
            [
                Icon(
                    icons.PERSON,
                    size=350,
                    color=colors.YELLOW_900
                )
            ],
            alignment='center'
        ),
        visible=True
    )

    login_value = TextField(
        label="LOGIN",
        border_width=3,
        border_radius=50,
        bgcolor=colors.WHITE12,
        border_color=colors.YELLOW_900,
        color=colors.YELLOW_900,
        selection_color=colors.BLUE_GREY_200,
    )
    login_textfield = Container(
        content=Row(
            [
                login_value
            ],
            alignment='center'
        ),
        padding=15,
        visible=True
    )

    password_value = TextField(
        label="SENHA",
        border_width=3,
        border_radius=50,
        bgcolor=colors.WHITE12,
        border_color=colors.YELLOW_900,
        color=colors.YELLOW_900,
        selection_color=colors.BLUE_GREY_200,
        password=True,
        can_reveal_password=True,
    )
    password_textfield = Container(
        content=Row(
            [
                password_value
            ],
            alignment='center',
        ),
        padding=20,
        visible=True
    )

    login_button = Container(
        content=Row(
            [
                IconButton(
                    icon_size=150,
                    on_click=lambda _: page.go("/user"),
                    icon=icons.LOGIN_ROUNDED,
                    tooltip="ENTRAR",
                    icon_color=colors.YELLOW_900
                ),

                IconButton(
                    icon_size=150,
                    on_click=lambda _: page.go("/register"),
                    icon=icons.HOW_TO_REG_ROUNDED,
                    tooltip="CADASTRAR",
                    icon_color=colors.YELLOW_900
                )
            ],
            alignment="center",
            spacing=200
        ),
        visible=True,
        top=80, right=180
        )
    
    login_appbar = AppBar(
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
                ),
            PopupMenuButton(
                IconButton(
                    icon=icons.PERSON_ROUNDED,
                    on_click=lambda _:page.go("/login"),
                ),
                tooltip='LOGIN'
            ),
        ]
    )
    
    page.update()

    return View(
        "/login",
        controls=[
            login_appbar, icon_login, login_textfield, password_textfield, Stack([login_button])
        ]
    )

def to_values_login():
    login = login_value.value
    password = password_value.value
    return login, password
