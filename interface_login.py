import flet as ft
from flet import *
# login_value = TextField(None)
# password_value = TextField(None)

def login(page: ft.Page):
    global login_value, password_value
    page.bgcolor = colors.BLACK12
    page.window_resizable = False
    page.window_width = 450
    page.window_height = 500

    icon_login = Container(
        content=Row(
            [
                Icon(
                    icons.PERSON,
                    size=170,
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
        can_reveal_password=True
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
    return icon_login, login_textfield, password_textfield


def to_values_login():
    login = login_value.value
    password = password_value.value
    return login, password
