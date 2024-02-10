import flet as ft
from flet import *
from flet_route import Params, Basket
from interface_user import get_historico_atual

LIGHT_SEED_COLOR = colors.DEEP_ORANGE
DARK_SEED_COLOR = colors.INDIGO

def view_historic(page: ft.Page, params=Params, basket=Basket):
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
    
    historico_atual = get_historico_atual()

    historic_movement = []
    for tupla in historico_atual:
        for transacao in tupla:
            tipo = transacao['tipo']
            if  tipo == 'Depósito' or  tipo == 'Saque':
                valor = transacao['valor']
                date_ = transacao['data']
                hora_ = transacao['hora']
                historic_movement.append({'tipo':tipo,'valor': valor,'date': date_,'hora': hora_})

    show_historic = Row(
        [
            Text(
                "HISTÓRICO",
                weight='bold',
                size=70,
                color=colors.YELLOW_900
            ),
        ],
        alignment=MainAxisAlignment.CENTER
    )

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
                            icon=icons.REPLAY_CIRCLE_FILLED,
                            on_click=lambda _: page.go("/user")
                        )

                    ),
                ]
            )
    
    # Lista para armazenar todas as transações
    show_transactions = []

    # Itera sobre todas as transações no histórico
    for key_deposit in historic_movement:
        type_deposit = key_deposit['tipo']
        value_deposit = key_deposit['valor']
        date_deposit = key_deposit['date']
        hora_deposit = key_deposit['hora']

        show_transaction = Container(
            content=Column(
                [
                    Text(
                        f"{type_deposit} R${value_deposit}, Data {date_deposit} {hora_deposit}",
                        color=colors.GREEN if type_deposit == 'Depósito' else colors.RED,
                        text_align=MainAxisAlignment.CENTER,
                        size=25 if type_deposit == 'Depósito' else 27
                    )
                ],
            ),
        )

        show_transacion_row = Row(
            [
                show_transaction,
            ],
            alignment=MainAxisAlignment.SPACE_AROUND
        )
        
        # Adiciona cada transação à lista de transações
        show_transactions.append(show_transacion_row)

    # Retorna a visualização completa do histórico
    return View(
        "/historic",
        controls=[
            page_appbar, show_historic, *show_transactions  # Usando * para descompactar a lista de transações
        ]
    )
