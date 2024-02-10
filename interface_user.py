import flet as ft
from flet import *
from flet_route import Params, Basket
from postgres_bd import conectar_bd
from psycopg2 import extras
from datetime import datetime
from validate_password import validate_password
from savings_account import create_savings
from interface_login import to_values_login

LIGHT_SEED_COLOR = colors.GREEN_900
DARK_SEED_COLOR = colors.GREEN_900

estado_replace_mode = False
email = "josimar_504@hotmail.com"
senha = "941402"
def user_interface(page: ft.Page, params=Params, basket=Basket):
    global id_cliente
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
    
    # email, senha = validate_click()
    validate_result = validate_password(email, senha)
    
    if validate_result == 'Senha válida!':
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
                size=30,
                width=200,
                weight='bold',
                text_align=TextAlign.END,
                visible=True
            )
        
        user_balance_off = Text(
                "****",
                size=30,
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
        

        # Definindo as funções para os dois comportamentos
        def replace_user_validado(e):
            page.go("/user_validado")

        def replace_user(e):
            page.go("/user")

        # Definindo a função que será chamada a cada clique no botão
        def toggle_replace_mode(e):
            global estado_replace_mode
            if estado_replace_mode:
                replace_user_validado(e)
            else:
                replace_user(e)
            # Alternando o estado para o próximo clique
            estado_replace_mode = not estado_replace_mode
        
        


        go_to_historic = Container(
            content=OutlinedButton(
                text='',
                width=350,
                scale=2,
                content=Row(
                    [Text(
                        'SALDO',
                        size=30,
                        width=100,
                        text_align=TextAlign.CENTER,
                        ),
                        user_balance_on,
                        user_balance_off
                    ],
                    alignment=MainAxisAlignment.SPACE_BETWEEN
                ),
                on_click=lambda _: page.go("/historic")
            ),
            top=100, right=230
        )


        user_name = Container(
            content=Row(
                [
                    Text(
                    value=f"Olá, {name.split()[0]}",
                    weight="bold",
                    italic=True,
                    color=colors.YELLOW_900,
                    size=25
                    )
                ],
                alignment='center'
            ),
            top=25, left=100,
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
                    icon_size=70,
                    icon_color=colors.GREEN_900,
                    width=70,
                    on_click=deposit_click
                ),
                IconButton(
                    icon=icons.ARROW_UPWARD_ROUNDED,
                    icon_size=70,
                    icon_color=colors.RED_700,
                    width=70,
                    on_click=withdraw_click
                )
            ],
            alignment=MainAxisAlignment.END,
            spacing=40
            ),
            top=200, left=120,
            visible=True
        )
        
        cash_movement_description = Container(
            width=600,
            content=Row(
                [
                    Text(
                        "DEPOSITAR   ",
                        color=colors.YELLOW_900,
                        weight="bold"
                    ),
                    Text(
                        "SACAR",
                        color=colors.YELLOW_900,
                        weight="bold"
                    )
                ],
                alignment=MainAxisAlignment.END,
                spacing=40
            ),
            top=300, left=120,
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
            top=200, left=565,
            visible=False,
        )
        
        icon_deposit = Container(
            width=200,
            content=Row(
                [
                    IconButton(
                        icon=icons.ADD,
                        icon_size=30,
                        bgcolor=colors.GREY,
                        on_click=deposit_click_movement ,
                        icon_color=colors.YELLOW_900
                    ),
                ],
                alignment=MainAxisAlignment.SPACE_EVENLY
            ),
            top=275, left=535,
            visible=False
        )

        icon_withdraw = Container(
            width=200,
            content=Row(
                [
                    IconButton(
                        icon=icons.ADD,
                        icon_size=30,
                        bgcolor=colors.GREY,
                        on_click=withdraw_click_movement,
                        icon_color=colors.YELLOW_900
                        
                    ),
                ],
                alignment=MainAxisAlignment.SPACE_EVENLY
            ),
            top=275, left=535,
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
                                IconButton(
                                    icon=icons.PERSON_ROUNDED,
                                    on_click=lambda _: page.go("/login"),
                                ),
                                tooltip='LOGIN'
                            ),
                            PopupMenuButton(
                                IconButton(
                                    icon=icons.REPLAY_ROUNDED,
                                    on_click=toggle_replace_mode
                                )
                            ),
                            PopupMenuButton(
                                balance_mode,

                            ),
                        ]
                    )
        page.add(page_appbar, Stack([user_name, cash_movement, cash_movement_description, go_to_historic, cash_withdraw_or_deposit_view, icon_deposit, icon_withdraw]))
        return View(
            "/user_validado",
            controls=[
                page_appbar, Stack([user_name, cash_movement, cash_movement_description, go_to_historic, cash_withdraw_or_deposit_view, icon_deposit, icon_withdraw])
            ]
        )

    elif validate_result == 'Senha inválida!':
        print("Falha na validação!")
        return View(
            "/user",
            controls=[
                Text(
                    "SENHA INVÁLIDA!"
                ),
                IconButton(
                    icon=icons.REPLAY_CIRCLE_FILLED,
                    on_click=lambda _: page.go("/login")
                )
            ]
        )
    elif validate_result == 'Email não encontrado.':
        return View(
            "/user",
            controls=[
                Text(
                    "Email não encontrado!"
                ),
                IconButton(
                    icon=icons.REPLAY_CIRCLE_FILLED,
                    on_click=lambda _: page.go("/login")
                )
            ]
        )
    else:
        print(f"Campo em branco!")
        return View(
            "/user",
            controls=[
                Text(
                    "ERROR!"
                ),
                IconButton(
                    icon=icons.REPLAY_CIRCLE_FILLED,
                    on_click=lambda _: page.go("/login")
                )
            ]
        )
    

    

    
def validate_click():
        login, password = to_values_login()
        email = login
        senha = password
        return email, senha

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

ft.app(target=user_interface)