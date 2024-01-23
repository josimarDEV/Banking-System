import flet as ft
from flet import *

from interface_login import login, to_values_login
from interface_register import register
from interface_register import insert_customer
from validate_password import validate_password


def main(page: ft.Page):
    page.bgcolor = colors.BLACK38
    page.window_resizable = False
    page.window_width = 450
    page.window_height = 500
    page.title = 'Banco Silva'
    page.horizontal_alignment = 'center'

    welcome = Container(
        content=Row(
            [
                Text(
                    'Seja Bem Vindo',
                    size=40,
                )
            ],
            alignment=alignment.center
        ),
        padding=100,
        visible=True
    )

    def login_click(e):
        page.clean()
        page.bgcolor = colors.BLACK38
        page.window_resizable = False
        page.window_width = 450
        page.window_height = 490
        page.horizontal_alignment = 'center'
        page.vertical_alignment = 'center'

        icon_login, login_textfield, password_textfield = login(e)
        page.add(icon_login, login_textfield, password_textfield, login_button)
        page.update()

    welcome_textfield = ft.Container(
        content=TextButton(
            'ENTRAR',
            on_click=login_click
        ),
        alignment=ft.alignment.center,
        width=80,
        height=60,
        visible=True
    )

    def register_click(e):
        page.clean()
        page.bgcolor = colors.BLACK38
        page.window_resizable = False
        page.window_width = 550
        page.window_height = 570
        page.horizontal_alignment = 'center'
        page.vertical_alignment = 'center'
        page.scroll = True

        cadastro_text, nome_textfield, cpf_textfield, email_textfield, telefone_textfield, data_nascimento_textfield, senha_textfield = register(
            e)
        register_event = Column(
            [
                cadastro_text,
                nome_textfield,
                cpf_textfield,
                email_textfield,
                telefone_textfield,
                data_nascimento_textfield,
                senha_textfield,
            ],
            visible=True,
        )

        to_add = Container(
            content=Row(
                [
                    IconButton(
                        icon=icons.ADD,
                        icon_color=colors.YELLOW_900,
                        icon_size=20,
                        bgcolor=colors.YELLOW_100,
                        on_click=lambda e: insert_customer(
                            nome_textfield.value,
                            cpf_textfield.value,
                            email_textfield.value,
                            telefone_textfield.value,
                            data_nascimento_textfield.value,
                            senha_textfield.value,  # Substitua pelo valor real para secret
                            0,  # Substitua pelo valor real para saldo
                            1,  # Substitua pelo valor real para id_tipo_conta
                            1  # Substitua pelo valor real para id_status_conta
                        )
                    )
                ],
                alignment='center',
            ),
            visible=True
        )

        page.add(register_event, to_add)
        page.update()

    def validate_click(e):
        login, password = to_values_login()
        email = login
        senha = password
        validate_result = validate_password(email, senha)
        if validate_result == 'Senha válida!':
            print("Validado com sucesso!")
        elif validate_result == 'Senha inválida!':
            print("Falha na validação!")
        elif validate_result == 'Email não encontrado.':
            print("Email não encontrado!")
        else:
            print(f"Campo em branco!")
        page.update()

    login_button = Container(
        content=Row(
            [
                TextButton(
                    "ENTRAR",
                    width=100,
                    height=50,
                    on_click=validate_click
                ),

                TextButton(
                    "CADASTRAR",
                    width=120,
                    height=50,
                    on_click=register_click
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY
        ),
        padding=15,
        visible=True
    )
    page.add(welcome, welcome_textfield)
    page.update(page)


ft.app(target=main)
