import flet as ft
from flet import *

from interface_login import login, to_values_login
from interface_register import register
from interface_register import insert_customer
from validate_password import validate_password
from savings_account import create_savings
from user_interface import user_interface

LIGHT_SEED_COLOR = colors.DEEP_ORANGE
DARK_SEED_COLOR = colors.INDIGO

def main(page: Page):
    def check_item_clicked(e):
        e.control.checked = not e.control.checked
        page.update()

    page.title = "Banco Silva"
    page.theme_mode = "light"
    page.window_resizable = False
    page.window_width = 600
    page.window_height = 500
    page.horizontal_alignment = MainAxisAlignment.CENTER
    page.theme = Theme(color_scheme_seed=LIGHT_SEED_COLOR, use_material3=True)
    page.dark_theme = Theme(color_scheme_seed=DARK_SEED_COLOR, use_material3=True)
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
                    size=50,
                    weight='bold',
                    color=colors.YELLOW_900
                )
            ],
            alignment='center'
        ),
        top=100, left=50,
        visible=True,
    )

    def login_click(e):
        page.clean()
        page.window_resizable = False
        page.window_width = 600
        page.window_height = 650
        page.horizontal_alignment = 'center'
        page.vertical_alignment = 'center'

        login_button = Container(
        content=Row(
            [
                TextButton(
                    "ENTRAR",
                    width=120,
                    height=50,
                    on_click=validate_click,
                    icon=icons.LOGIN_ROUNDED
                ),

                TextButton(
                    "CADASTRAR",
                    width=150,
                    height=50,
                    on_click=register_click,
                    icon=icons.HOW_TO_REG_ROUNDED
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY
        ),
        padding=15,
        visible=True,
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
                        on_click=login_click,
                    ),
                    tooltip='LOGIN'
                ),
            ]
        )
        
        icon_login, login_textfield, password_textfield = login(e)
        page.add(login_appbar, icon_login, login_textfield, password_textfield, login_button)
        page.update()

    welcome_textfield = ft.Container(
        content=Row(
            [
                TextButton(
                    'ENTRAR',
                    height=40,
                    width=120,
                    icon=icons.LOGIN,
                    icon_color=colors.GREEN_900,
                    on_click=login_click
                ),
            ],
            alignment=MainAxisAlignment.CENTER,
        ),
        top=285, left=175, bgcolor=colors.YELLOW_900, border_radius=50,
        )

    def register_click(e):
        page.clean()
        page.window_resizable = False
        page.window_width = 840
        page.window_height = 920
        page.horizontal_alignment = MainAxisAlignment.CENTER
        page.scroll = True

        cadastro_text, nome_textfield, cpf_textfield, email_textfield, telefone_textfield, data_nascimento_textfield, senha_textfield, option_email = register(
            e)

        register_event = Column(
            [
                cadastro_text,
                nome_textfield,
                cpf_textfield,
                Row(
                    [email_textfield,
                    option_email]
                ),
                telefone_textfield,
                data_nascimento_textfield,
                senha_textfield,
            ],
            visible=True,
            alignment='center'
        )

        to_add = Container(
            content=Row(
                [
                    IconButton(
                        icon=icons.ADD,
                        icon_size=30,
                        bgcolor=colors.YELLOW_900,
                        on_click=lambda e: insert_customer(
                            nome_textfield.value.title(),
                            cpf_textfield.value,
                            f"{email_textfield.value}{option_email.value}",
                            telefone_textfield.value,
                            data_nascimento_textfield.value,
                            senha_textfield.value,  # Substitua pelo valor real para secret
                            1,  # Substitua pelo valor real para id_tipo_conta
                            1  # Substitua pelo valor real para id_status_conta
                        )
                    )
                ],
                alignment='center'
            ),
            visible=True
        )

        register_appbar = AppBar(
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
                        on_click=login_click,
                    ),
                    tooltip='LOGIN'
                ),
            ]
        )

        page.add(register_appbar, register_event, to_add)
        page.update()

    def validate_click(e):
        login, password = to_values_login()
        email = login
        senha = password
        validate_result = validate_password(email, senha)
        if validate_result == 'Senha válida!':
            page.clean()
            balance_mode, controlers, user_name, user_balance_on, user_balance_off, cash_movement, cash_movement_description, cash_withdraw_or_deposit_view, icon_deposit, icon_withdraw = user_interface(page, email)
            
            page_appbar = AppBar(
                bgcolor=colors.YELLOW_900,
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
                                on_click=login_click,
                            ),
                            tooltip='LOGIN'
                        ),
                        PopupMenuButton(
                            IconButton(
                                icon=icons.REPLAY_ROUNDED,
                                on_click=validate_click
                            )
                        ),
                        PopupMenuButton(
                            balance_mode,

                        ),
                    ]
                )
            page.add(page_appbar, Stack([user_name, cash_movement, cash_movement_description, controlers, cash_withdraw_or_deposit_view, icon_deposit, icon_withdraw]))
            create_savings(email)

        elif validate_result == 'Senha inválida!':
            print("Falha na validação!")
        elif validate_result == 'Email não encontrado.':
            print("Email não encontrado!")
        else:
            print(f"Campo em branco!")
        page.update()

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
                ),
            PopupMenuButton(
                IconButton(
                    icon=icons.PERSON_ROUNDED,
                    on_click=login_click,
                ),
                tooltip='LOGIN'
            ),
        ]
    )
    page.add(interface_appbar, Stack([welcome_textfield, welcome], height=350))
    page.update(page)

ft.app(target=main)
