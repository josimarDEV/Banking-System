import random # importa  a função random para gerar números aleatórios
import string #  importa a classe string que possui várias strings de caracteres especiais


import flet as ft
from flet import *
from flet_route import Params, Basket
from postgres_bd import conectar_bd
from create_table import create_table #  importa o módulo criador de tabelas do banco de dados
import re #  importa a biblioteca regular expression (regex) para realizar expressões regulares

LIGHT_SEED_COLOR = colors.DEEP_ORANGE
DARK_SEED_COLOR = colors.INDIGO

def register(page: ft.Page, params=Params, basket=Basket):
    global nome_textfield, cpf_textfield, email_textfield, telefone_textfield, data_nascimento_textfield, senha_textfield
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

    cadastro_text = Row(
        [
            Text(
                "CADASTRO",
                size=100,
                color=colors.YELLOW_900,
                weight='bold',
            )
        ],
        alignment='center',
    )

    nome_textfield = TextField(
        label='NOME',
        hint_text='Nome Completo', #  placeholder="Digite o seu nome completo...",
        helper_text='Nome Completo', # helper texto para explicar o que é esse campo
        border_width=3,
        border_radius=50,
        width=700,
        border_color=colors.YELLOW_900,
        color=colors.YELLOW_900,
        bgcolor=colors.WHITE12
    )

    cpf_textfield = TextField(
        label='CPF',
        hint_text='00000000000',
        helper_text='Somente Números',
        border_width=3,
        border_radius=50,
        width=700,
        border_color=colors.YELLOW_900,
        color=colors.YELLOW_900,
        bgcolor=colors.WHITE12
    )

    email_textfield = TextField(
        label='EMAIL',
        hint_text='exemplo_2024',
        helper_text='email sem o @',
        border_width=3,
        border_radius=50,
        width=500,
        border_color=colors.YELLOW_900,
        color=colors.YELLOW_900,
        bgcolor=colors.WHITE12

    )

    telefone_textfield = TextField(
        label='TELEFONE',
        hint_text='28999707070',
        helper_text='Somente Números',
        border_width=3,
        border_radius=50,
        width=700,
        border_color=colors.YELLOW_900,
        color=colors.YELLOW_900,
        bgcolor=colors.WHITE12
    )

    data_nascimento_textfield = TextField(
        label='DATA DE NASCIMENTO',
        hint_text='14021994',
        helper_text='Somente Números',
        border_width=3,
        border_radius=50,
        width=700,
        border_color=colors.YELLOW_900,
        color=colors.YELLOW_900,
        bgcolor=colors.WHITE12
    )
    senha_textfield = TextField(
        label='SENHA',
        hint_text='senha será criptografada...',
        helper_text='Senha Maior de 8 Digítos',
        password=True,
        can_reveal_password=True,
        border_width=3,
        border_radius=50,
        width=700,
        border_color=colors.YELLOW_900,
        color=colors.YELLOW_900,
        bgcolor=colors.WHITE12
    )

    option_email = Dropdown( #  Opção para escolher o tipo de e-mail a ser cadastrado.
        width=190,
        label='@',
        border_radius=30,
        border_width=3,
        border_color=colors.YELLOW_900,
        bgcolor=colors.WHITE12,
        color=colors.YELLOW_900,
        helper_text="hotmail,gmail,outlook",
        options=[
            dropdown.Option("@hotmail.com"), # opções de email para ser escolhido
            dropdown.Option("@gmail.com"),
            dropdown.Option("@outlook.com"),
        ],
    )
    
    register_event = Column( # coloca as variaceis em colunas
            [
                nome_textfield,
                cpf_textfield,
                Row( # coloca  os dois campos do email na mesma linha
                    [email_textfield,
                    option_email]
                ),
                telefone_textfield,
                data_nascimento_textfield,
                senha_textfield,
            ],
            visible=True,
        )
    register_event_ = Container( # para o register_event ser manipulado
        content=Row(
            [
                register_event
            ],
            alignment=MainAxisAlignment.CENTER
        )
    )
    to_add = Container(
        content=Row(
            [
                IconButton(
                    icon=icons.ADD,
                    icon_color=colors.YELLOW_900,
                    icon_size=30,
                    bgcolor=colors.GREY,
                    on_click=lambda e: insert_customer( #quando clickado gera o evento de inserir os dados no banco de dados
                        nome_textfield.value.title(),
                        cpf_textfield.value,
                        f"{email_textfield.value}{option_email.value}", #  concatenação dos valores das duas  caixas de texto
                        telefone_textfield.value,
                        data_nascimento_textfield.value,
                        senha_textfield.value,
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
                    on_click=lambda _: page.go("/login"),
                ),
                tooltip='LOGIN'
            ),
        ]
    )

    page.update()
    return View(
        "/register",
        controls= [
            register_appbar, cadastro_text, Stack([register_event_]), to_add
        ]
    )
def cpf_validado(cpf): # validada ser o cpf digitado já existi, comparando com o cpfs no banco de dados
    conn = conectar_bd()
    cur = conn.cursor()

    query = "SELECT cpf FROM clientes WHERE cpf = %s"
    cur.execute(query, (cpf,))
    cpf_validado = cur.fetchall()

    cur.close()
    conn.close()

    return bool(cpf_validado)  # Verifica se a lista não está vazia


def email_validado(email): # aqui valida o email , verificando se ele existe no banco de dados
    conn = conectar_bd()
    cur = conn.cursor()

    query = "SELECT email FROM clientes WHERE email = %s"
    cur.execute(query, (email,))
    email_validado = cur.fetchall()

    cur.close()
    conn.close()

    return bool(email_validado)  # Verifica se a lista não está vazia


def insert_customer(nome, cpf, email, telefone, data_nascimento, senha,
                    id_tipo_conta, id_status_conta): # função para inseir o cliente no banco de dados
    create_table() # chama a função criar  tabela caso ela ainda não tenha sido criada
    # parte que tem umas tratativas de erros, ainda pode ser burlado!
    if cpf_validado(cpf):
        print("ERROR: CPF já cadastrado")
        return

    if email_validado(email):
        print("ERROR: E-mail já cadastrado")
        return

    if nome == "":
        print("Campo do Nome vazio!")
    elif cpf == "":
        print("Campo do CPF vazio!")
    elif email == "":
        print("Campo do Email vazio!")
    elif telefone == "":
        print("Campo do Telefone vazio!")
    elif data_nascimento == "":
        print("Campo do Data de Nascimento vazio!")
    elif senha == "":
        print("Campo do Senha vazio!")
    elif len(senha) < 8:
        print("Senha deve ser maior que 8 digitos")
    else:
        def validar_email(email):
            # Verificar se o e-mail contém apenas caracteres válidos
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                return False

            # Verificar se o domínio do e-mail é permitido (hotmail.com, gmail.com, outlook.com)
            dominios_permitidos = ["hotmail.com", "gmail.com", "outlook.com"]
            dominio = email.split("@")[1]

            if dominio not in dominios_permitidos:
                return False

            return True

        # Chama validar email si retorna True ele faz todo o caminho até inserir os dados no banco de dados.
        if validar_email(email) is True:
            try:
                conn = conectar_bd()
                cur = conn.cursor()

                cpf = cpf.replace(" ", "").replace("-", "").replace("/", "") # retira espaços e caracteres que poderia sr usado para ser tratado
                cpf_formatado = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}" # formata o cpf  para o padrão brasileiro

                telefone = telefone.replace(" ", "").replace("-", "").replace("/", "")
                telefone_formatado = f"({telefone[:2]}){telefone[2:7]}-{telefone[7:]}"

                data_nascimento = data_nascimento.replace(" ", "").replace("-", "").replace("/", "")
                data_nascimento_formatado = f"{data_nascimento[:2]}/{data_nascimento[2:4]}/{data_nascimento[4:]}"

                if nome and cpf_formatado and email and telefone_formatado and data_nascimento_formatado and senha: # verifica si contem tudo corretanmente, caso sim avança
                    def secret(): # essa função é para criptografar a senha
                        a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                            's','t','u', 'v', 'w', 'x', 'y', 'z']
                        b = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
                        c = list("!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")

                        alfa = []

                        for _ in range(200): # escolhe aleatoriamente caracteres e coloca na lista alfa... cada usuario é único
                            alfa.append(random.choice(a))
                            alfa.append(random.choice(b))
                            alfa.append(random.choice(c))

                        alfa = ''.join(map(str, alfa)) # retira da lista tranformando em uma string
                        return alfa

                    def get_values_secret_max(): # usa caracteres maiusculas para  gerar uma parte da senha secreta
                        values_max = list(string.ascii_uppercase) # pega uma lista  com todos os valores possíveis de letras maiusculas
                        especial_characters = string.punctuation #  pega todos os caractéres especiais
                        values_max += especial_characters # adiciona na string com os caracteres especiais
                        random.shuffle(values_max) #  embaralhar os caracteres
                        max_secret = ''.join(map(str, values_max))
                        return max_secret

                    def get_values_secret_min(): # essa parte é minusculas
                        values_min = list(string.ascii_lowercase)
                        especial_characters = string.punctuation
                        values_min += especial_characters
                        random.shuffle(values_min)
                        min_secret = ''.join(map(str, values_min))
                        return min_secret

                    alfa = secret()

                    def get_values_secrets(): # essa parte já cria uma senha secreta completa
                        choice_values_secrets = []

                        secret_min = list(min_secret) # tranforma tudo em lista
                        secret_max = list(max_secret)
                        nome_secret = list(nome)
                        phone_secret = list(telefone_formatado)
                        password_secret = list(senha)
                        data_secret = list(data_nascimento_formatado)

                        password_index = 0 # são os indices iniciais
                        secret_max_index = 0
                        secret_min_index = 0
                        data_index = 0
                        nome_secret_index = 0
                        phone_secret_index = 0

                        for i in range(len(alfa)): # nesta parte cria a senha, usando as variaveis acima, com base em localidades padrão
                            if i % 5 == 0 and nome_secret and nome_secret_index < len(nome_secret): #  se o indice for divisivel por 5, e nome_secret e nome_secret_index for menor que o tamanho de nome secreto faz oque é pedido abaixo 
                                choice_values_secrets.append(nome_secret[nome_secret_index]) # lembra se a parte de cima trata um erro de nome_secret de chegar em seu ultimo caracter e ocorre erro que não pode inserir mais pois cabaou os caracteres.
                                nome_secret_index += 1 # acima coloca o carater do indice inicial na lista choice_values_secrets, sempre que pasa aqui o indice aumenta + 1
                            elif i % 11 == 3 and phone_secret and phone_secret_index < len(phone_secret):
                                choice_values_secrets.append(phone_secret[phone_secret_index])
                                phone_secret_index += 1
                            elif i % 7 == 1 and password_secret and password_index < len(password_secret):
                                choice_values_secrets.append(password_secret[password_index])
                                password_index += 1
                            elif i % 2 == 0 and secret_max and secret_max_index < len(secret_max):
                                choice_values_secrets.append(secret_max[secret_max_index])
                                secret_max_index += 1
                            elif i % 3 == 2 and secret_min and secret_min_index < len(secret_min):
                                choice_values_secrets.append(secret_min[secret_min_index])
                                secret_min_index += 1
                            elif i % 19 == 4 and data_secret and data_index < len(data_secret):
                                choice_values_secrets.append(data_secret[data_index])
                                data_index += 1
                            else:
                                choice_values_secrets.append(alfa[i]) # caso não entra  nas condições acima, o caracter de alfa e jogado para a lista
                        return choice_values_secrets

                    max_secret = get_values_secret_max()
                    min_secret = get_values_secret_min()

                    salt = get_values_secrets()
                    password_secret = ''.join(map(str, salt)).replace(' ', '').replace('\n', '')

                    query_customers = """
                        INSERT INTO clientes (nome, cpf, email, telefone, data_nascimento, secret, id_tipo_conta, id_status_conta) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING id
                        """ # inseri os dados do cliente no banco de dados

                    query_secret_alfa = """
                        INSERT INTO secret_alfa (id_cliente, alfa)
                        VALUES (%s, %s)
                        """ # inseri a alfa gerado, pois cada alfa é unico, para ser usada quando o cliente for fazer login

                    query_secret_max = """
                        INSERT INTO max_secret (id_cliente, max_alfa) 
                        VALUES (%s, %s)
                        """

                    query_secret_min = """
                        INSERT INTO min_secret (id_cliente, min_alfa)
                        VALUES (%s, %s)
                        """
                    values_customer = (
                        nome, cpf_formatado, email, telefone_formatado, data_nascimento_formatado, password_secret,
                        id_tipo_conta, id_status_conta
                    ) # valores a ser pego na interface de cadastro do usuario

                    cur.execute(query_customers, values_customer) #  executa o comando sql para cadastrar um novo cliente
                    id_cliente = cur.fetchone()[0] #  pega o id gerado pelo banco para o novo registro, pois sera usado abaixo

                    values_secret_alfa = (id_cliente, alfa) # nesta parte para ser inserido tudo, precisando do id criado assim que o cliente cadastrar
                    values_secret_max = (id_cliente, max_secret)
                    values_secret_min = (id_cliente, min_secret)

                    cur.execute(query_secret_alfa, values_secret_alfa)
                    cur.execute(query_secret_max, values_secret_max)
                    cur.execute(query_secret_min, values_secret_min)

                    conn.commit() #  confirma as transações no banco de dados

                    print("Clientes inseridos com sucesso!")

                else:
                    print("Todos os campos obrigatórios devem ser preenchidos.")

            except Exception as e:
                print(f"Erro ao inserir cliente: {e}")
            finally:
                cur.close()
                conn.close()
        # si retorna False retorna uma mensagem de erro
        else:
            print(f"Email {email} não foi validado!")
            return 'Erro 502'
        