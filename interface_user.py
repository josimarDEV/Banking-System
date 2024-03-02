import flet as ft
from flet import *
from flet_route import Params, Basket
from postgres_bd import conectar_bd # importa a função de conexão com o banco de dados PostgreSQL
from psycopg2 import extras # permite que os resultados sejam retornado como dicionários em vez de tuplas.
from datetime import datetime #  para pegar a data atual
from validate_password import validate_password
from savings_account import create_savings
from interface_login import to_values_login

LIGHT_SEED_COLOR = colors.GREEN_900
DARK_SEED_COLOR = colors.GREEN_900
senha = "941402"
email = "josimar_504@hotmail.com"
estado_replace_mode = False # define uma variavel  global

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
    
    email, senha = validate_click() # variaveis  que recebem os dados do usuario de  login
    validate_result = validate_password(email, senha)  # valida se o usuário e senha estão corretos 
    
    if validate_result == 'Senha válida!': # verifica se o resultado retornado é iqual a "senha válida!"
        def get_id_client(email):
            conn = conectar_bd() # conecta com o banco de dados
            cur = conn.cursor()

            try: # tenta executar o comando sql
                query = "SELECT id FROM clientes WHERE email = %s" # busca no banco de dados  o id do cliente correspondente ao email digitado
                cur.execute(query, (email,)) # executa o comando de cima no banco de dados passando como parametro o email digitado pelo usuario em login
                id_cliente = cur.fetchone() # pega o id do cliente
                if id_cliente: # verifica si o cliente tem id, ou seja, já existe no sistema
                    return id_cliente[0]  # retorna o id do cliente dono do email informado
            except Exception as e: #  em caso de erro exibe na tela, porém não coloquei esse retorno para ser exibido, mais seria viavel, com o return view()
                print(f"Erro ao obter id do cliente: {e}")
            finally:
                cur.close() # fecha a conexão com o banco de dados
                conn.close()

        def name_client(email):
            conn = conectar_bd()
            cur = conn.cursor()
            
            try:
                query = "SELECT nome FROM clientes WHERE email = %s"
                cur.execute(query, (email,))
                nome = cur.fetchone()[0]
                if nome:
                    return str(nome) # str faz com que retorne a variavel como string
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
                    return float(balance[0])   # converte o valor para float
            except Exception as e:
                print(f"Erro na consulta de saldo da conta poupança: {e}")
            finally:
                cur.close()
                conn.close()


        id_cliente = get_id_client(email) # cria uma variavel com o retorno  da função get_id_client
        name = name_client(email)
        balance = client_balance(id_cliente)
        balance_str = f"R${balance:.2f}" if balance is not None else "N/A" # reformata o saldo do cliente com a condição de ele nao retornar None
        
        user_balance_on = Text(
                f"{balance_str}", # mostar a variavel reformatada para ser mostrado na pagina
                size=30,
                width=200,
                weight='bold',
                text_align=TextAlign.END,
                visible=True
            )
        
        user_balance_off = Text( # criei uma segunda interface texto para quando não quiser mostrar o saldo, pois como estou aprendendo a programar foi o unico jeito que pensei
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


        def hide_balance(e): # essa funçao criada  é chamada quando o botao for pressionado
            balance_mode.icon = (
                icons.VISIBILITY if user_balance_on.visible == False else  icons.VISIBILITY_OFF 
            )
            user_balance_on.visible = not user_balance_on.visible # inverte o valor de visivel do elemento
            user_balance_off.visible = not user_balance_off.visible
            page.update()

        balance_mode = IconButton(
        icons.VISIBILITY if user_balance_on.visible == True else  icons.VISIBILITY_OFF,
            on_click=hide_balance
            ) # estado padrão do icone 
        page.padding = 30
        

        # Definindo as funções para os dois comportamentos
        def replace_user_validado(e):
            page.go("/user_validado")

        def replace_user(e):
            page.go("/user")

        # Definindo a função que será chamada a cada clique no botão
        def toggle_replace_mode(e): # achei um bug quando clicava no icone  e não mudava de tela, essa foi a solução
            global estado_replace_mode
            if estado_replace_mode:
                replace_user_validado(e)
            else:
                replace_user(e)
            # Alternando o estado para o próximo clique
            estado_replace_mode = not estado_replace_mode
        
        


        go_to_historic = Container( # pensei nessa parte utilizando o app da nubank, verifiquei que qualquer clicke no saldo, mostrava outra tela
            content=OutlinedButton( # entao crie um botao sem nada, que tivesse as informaçoes do saldo
                text='',
                width=350,
                scale=2, # escala do tamanho do botao, para 2x
                content=Row(
                    [Text(
                        'SALDO',
                        size=30,
                        width=100,
                        text_align=TextAlign.CENTER,
                        ),
                        user_balance_on, # chamei as vairaveis de fora da funcao pra poderem mostrar o saldo, uma mostra e a ontra esconde
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
                    value=f"Olá, {name.split()[0]}", # pega apenas o primeiro nome utilizando split que tranforma o nome completo em uma lista, e pego a posição do primeiro nome que é 0
                    weight="bold",
                    italic=True, #  fazer a letra estar em itálico
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
            date = datetime.now() # pega a data e hora atual, mais aqui tambem pega a hora
            date_ = date.strftime("%d-%m-%Y") # manipula a data atual para mostrar somente a data
            hora_ = date.strftime("%H:%M:%S") #  manipula a data para mostrar apenas as horas
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
                params = (extras.Json(historico_atual), id_cliente) #  Passa os valores da variável historico_atual como um JSON e o ID do usuario, retornando como dicionario

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
            deposit_value = ''.join(map(str, cash_withdraw_or_deposit.value)) #  Transformar a string em um número
            deposit_value = float(deposit_value) # transforma  a string em um valor numérico para ser manipulado com paramentros matematicos

            if deposit_value > 0: # verifica se o valor  é maior que zero
                value_client += deposit_value # adiciona no saldo do cliente  o valor da depósito tipo é assim::::::>> exemplo... valor do saldo do cliente = valor do saldo do cliente + valor informado para ser adicionado
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
                value_client -= withdraw_value # quase a mesma coisa como o deposito, a diferença é que subtrai pois esta retirando valor da conta
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



        def deposit_click(e): # essa funçao esconde as variaveis e mostra outras, para ficar mais dinamica a interface
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

        cash_withdraw_or_deposit = TextField( # textfield para digitar a quantia que será depositada ou sacado
            label='valor',
            hint_text="somente número", # exibe o texto quando não há valor digitado, para informar o cliente alguma restrição, ou que será digitado
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
        return View( # isso sim aparece na tela como uma mensagem caso ele erre a senha, tem como de fazer como pop up
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
    

    

    
def validate_click(): # funçao criada para pegar o email e senha informados na hora de efetuar o login, estava chamando sem uma função  porem dava muito erro.
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
