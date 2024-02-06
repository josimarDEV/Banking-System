import flet as ft
from flet import *
from postgres_bd import conectar_bd
from psycopg2 import extras
from datetime import datetime

LIGHT_SEED_COLOR = colors.DEEP_ORANGE
DARK_SEED_COLOR = colors.INDIGO


def user_interface(page: ft.Page, email):
    page.window_width = 600
    page.window_height = 620
    page.window_resizable = False
    page.theme = Theme(color_scheme_seed=LIGHT_SEED_COLOR, use_material3=True)
    page.dark_theme = Theme(color_scheme_seed=DARK_SEED_COLOR, use_material3=True)
    page.update()

    def get_id_client(email):
        conn = conectar_bd()
        cur = conn.cursor()

        try:
            query = "SELECT id FROM clientes WHERE email = %s"
            cur.execute(query, (email,))
            id_cliente = cur.fetchone()
            if id_cliente:
                return id_cliente[0]
        except Exception as e:
            print(f"Erro ao obter id do cliente: {e}")
        finally:
            cur.close()
            conn.close()

    def name_client(email):
        conn = conectar_bd()
        cur = conn.cursor()
        
        try:
            query = "SELECT nome FROM clientes WHERE email = %s"
            cur.execute(query, (email,))
            nome = cur.fetchone()[0]
            if nome:
                return str(nome)
        except Exception as e:
            print(f"Erro ao obter  o nome do usuário: {e}")
        finally:
            cur.close()
            conn.close()

    def client_balance(id_cliente):
        conn = conectar_bd()
        cur = conn.cursor()
        
        try:
            query = "SELECT saldo FROM conta_poupanca WHERE id_cliente = %s"
            cur.execute(query, (id_cliente,))
            balance = cur.fetchone()
            if balance:
                return float(balance[0]) 
        except Exception as e:
            print(f"Erro na consulta de saldo da conta poupança: {e}")
        finally:
            cur.close()
            conn.close()


    id_cliente = get_id_client(email)
    name = name_client(email)
    balance = client_balance(id_cliente)
    balance_str = f"R${balance:.2f}" if balance is not None else "N/A"
    
    user_balance_on = Text(
            f"{balance_str}",
            size=50,
            width=350,
            weight='bold',
            text_align=TextAlign.END,
            visible=True
        )
    
    user_balance_off = Text(
            "****",
            size=50,
            width=200,
            weight='bold',
            text_align=TextAlign.END,
            visible=False
        )
    
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


    def hide_balance(e):
        balance_mode.icon = (
            icons.VISIBILITY if user_balance_on.visible == False else  icons.VISIBILITY_OFF
        )
        user_balance_on.visible = not user_balance_on.visible
        user_balance_off.visible = not user_balance_off.visible
        page.update()

    balance_mode = IconButton(
    icons.VISIBILITY if user_balance_on.visible == True else  icons.VISIBILITY_OFF,
        on_click=hide_balance
        )

    page.padding = 30

    def view_historic(e):
        page.clean()
        page.window_width = 600
        page.window_height = 620
        page.scroll = True

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

        page.add(show_historic)
        
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

            page.add(Row(
                [
                    show_transaction,
                ],
                alignment=MainAxisAlignment.SPACE_AROUND
            ))
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
                                icon=icons.PERSON,
                                on_click=deposit_click
                            )

                        ),
                    ]
                )
        page.add(page_appbar)
        
    controlers = Container(
        width=585,
        height=100,
        bgcolor=colors.YELLOW_900,
        content=OutlinedButton(
            text='',
            content=Row(
                [Text(
                    'SALDO',
                    size=50,
                    width=160,
                    text_align=TextAlign.CENTER,
                    ),
                    user_balance_on,
                    user_balance_off
                ],
                alignment=MainAxisAlignment.SPACE_BETWEEN
            ),
            on_click=view_historic
        ),
        top=20, right=-30
    )
    user_name = Container(
        content=Row(
            [
                Text(
                value=f"Olá, {name.title()}",
                )
            ],
            alignment='center'
        ),
        top=-22, left=5,
        visible=True,
    )

    def historic(tipo, deposit_value):
        date = datetime.now()
        date_ = date.strftime("%d-%m-%Y")
        hora_ = date.strftime("%H:%M:%S")
        # Conectando ao banco de dados
        conn = conectar_bd()
        cur = conn.cursor()

        # Obter o histórico atual do banco de dados
        historico_atual = get_historico_atual()
        if  historico_atual[0] is None:
            novo_historico = {"data": date_, "hora": hora_, "tipo": tipo, "valor": deposit_value}
            # Converter o histórico atual para uma lista vazia
            historico_atual = []            
            # Adicionando o novo histórico à lista existente
            historico_atual = [novo_historico]

        else:
            novo_historico = {"data": date_, "hora": hora_, "tipo": tipo, "valor": deposit_value}
            # Converter o histórico atual para uma lista
            historico_atual = list(historico_atual[0]) if historico_atual else []

            # Adicionando o novo histórico à lista existente
            historico_atual.append(novo_historico)

        try:
            # Atualizando o histórico na linha existente
            query = """
                UPDATE conta_poupanca 
                SET historico = %s
                WHERE id_cliente =  %s;
            """
            params = (extras.Json(historico_atual), id_cliente)

            cur.execute(query, params)
            conn.commit()
            print("Histórico atualizado com sucesso!")
        except Exception as e:
            print(f"Erro ao atualizar histórico: {e}")
        finally:
            cur.close()
            conn.close()

        
    def get_historico_atual():
        # Função para obter o histórico atual do banco de dados
        conn = conectar_bd()
        cur = conn.cursor()

        try:
            query = "SELECT historico FROM conta_poupanca WHERE id_cliente = %s"
            cur.execute(query, (id_cliente,))
            historico_atual = cur.fetchone()
            if historico_atual:
                return historico_atual
            else:
                return
        except Exception as e:
            print(f"Erro ao obter histórico atual: {e}")
        finally:
            cur.close()
            conn.close()

    def deposit_click_movement(e):
        balance = client_balance(id_cliente)
        value_client = float(balance)
        deposit_value = ''.join(map(str, cash_withdraw_or_deposit.value))
        deposit_value = float(deposit_value)

        if deposit_value > 0:
            value_client += deposit_value
            conn = conectar_bd()
            cur = conn.cursor()

            try:
                tipo = "Depósito"
                historic(tipo, deposit_value)
                query = "UPDATE conta_poupanca SET saldo =  %s WHERE id_cliente = %s"
                params = (value_client, id_cliente)

                cur.execute(query, params)
                conn.commit()
                print("Valor inserido com sucesso!")
                return float(value_client)
            except Exception as e:
                print(f"Erro! Ao inserir valor {e}")
            finally:
                cur.close()
                conn.close()
        else:
            print(f"Valor {value_client} incorreto. Verifique e tente novamente")
        page.update()


    def withdraw_click_movement(e):
        balance = client_balance(id_cliente)
        value_client = float(balance)
        withdraw_value = ''.join(map(str, cash_withdraw_or_deposit.value))
        withdraw_value = float(withdraw_value)

        if withdraw_value > 0:
            value_client -= withdraw_value
            conn = conectar_bd()
            cur = conn.cursor()
            
            try:
                tipo = "Saque"
                historic(tipo, withdraw_value)
                query = "UPDATE conta_poupanca SET saldo = %s WHERE id_cliente = %s"
                params = (value_client, id_cliente)
                
                cur.execute(query, params)
                conn.commit()
                print("valor retirado com sucesso!")
            except Exception as e:
                print(f"Erro! ao inserir valor {e}")
            finally:
                cur.close()
                conn.close()
        else:
            print(f"Valor {value_client} incorreto veridique e tente novamente")
        page.update()



    def deposit_click(e):
        cash_movement.visible = False
        cash_movement_description.visible = False
        cash_withdraw_or_deposit_view.visible = True
        icon_deposit.visible = True
        page.update()

    def withdraw_click(e):
        cash_movement.visible = False
        cash_movement_description.visible = False
        cash_withdraw_or_deposit_view.visible = True
        icon_withdraw.visible = True
        page.update()

    cash_movement = Container(
        width=600,
        content=Row(
        [
            IconButton(
                icon=icons.ARROW_DOWNWARD_ROUNDED,
                icon_size=50,
                icon_color=colors.GREEN_900,
                width=70,
                on_click=deposit_click
            ),
            IconButton(
                icon=icons.ARROW_UPWARD_ROUNDED,
                icon_size=50,
                icon_color=colors.RED_700,
                width=70,
                on_click=withdraw_click
            )
        ],
        alignment=MainAxisAlignment.END
        ),
        top=130, left=-50,
        visible=True
    )
    
    cash_movement_description = Container(
        width=600,
        content=Row(
            [
                Text(
                    "DEPOSITAR   ",
                ),
                Text(
                    "SACAR"
                )
            ],
            alignment=MainAxisAlignment.END
        ),
        top=200, left=-60,
        visible=True
    )

    cash_withdraw_or_deposit = TextField(
        label='valor',
        hint_text="somente número",
        width=150,
        border=3,
        border_color=colors.YELLOW_900,
        border_radius=50,
        bgcolor=colors.GREY_900,
        color=colors.YELLOW_900
    )

    cash_withdraw_or_deposit_view = Container(
        width=600,
        content=Column(
            [
                cash_withdraw_or_deposit,
            ],
            alignment=MainAxisAlignment.CENTER
        ),
        top=138, left=400,
        visible=False,
    )
    
    icon_deposit = Container(
        width=200,
        content=Row(
            [
                IconButton(
                    icon=icons.ADD,
                    icon_size=30,
                    bgcolor=colors.YELLOW_900,
                    on_click=deposit_click_movement 
                ),
            ],
            alignment=MainAxisAlignment.SPACE_EVENLY
        ),
        top=210, left=375,
        visible=False
    )

    icon_withdraw = Container(
        width=200,
        content=Row(
            [
                IconButton(
                    icon=icons.ADD,
                    icon_size=30,
                    bgcolor=colors.YELLOW_900,
                    on_click=withdraw_click_movement
                    
                ),
            ],
            alignment=MainAxisAlignment.SPACE_EVENLY
        ),
        top=210, left=375,
        visible=False
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
                            balance_mode,

                        ),
                    ]
                )
    
    # page.add(page_appbar, Stack([user_name, cash_movement, cash_movement_description, controlers, cash_withdraw_or_deposit_view, icon_deposit, icon_withdraw]))
    return balance_mode, controlers, user_name, user_balance_on, user_balance_off, cash_movement, cash_movement_description, cash_withdraw_or_deposit_view, icon_deposit, icon_withdraw

