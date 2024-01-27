import random
import string

import flet as ft
from flet import *
from postgres_bd import conectar_bd
from create_table import create_table
import re


def register(page: ft.Page):
    global nome_textfield, cpf_textfield, email_textfield, telefone_textfield, data_nascimento_textfield, senha_textfield

    cadastro_text = Row(
        [
            Text(
                "CADASTRO",
                size=60,
                color=colors.YELLOW_900,
                weight='bold',
            )
        ],
        alignment='center',
    )

    nome_textfield = TextField(
        label='NOME',
        hint_text='Nome Completo',
        helper_text='Nome Completo',
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

    option_email = Dropdown(
        width=190,
        label='@',
        border_radius=30,
        border_width=3,
        border_color=colors.YELLOW_900,
        bgcolor=colors.WHITE12,
        color=colors.YELLOW_900,
        helper_text="hotmail,gmail,outlook",
        options=[
            dropdown.Option("@hotmail.com"),
            dropdown.Option("@gmail.com"),
            dropdown.Option("@outlook.com"),
        ],
    )
    
    return cadastro_text, nome_textfield, cpf_textfield, email_textfield, telefone_textfield, data_nascimento_textfield, senha_textfield, option_email


def cpf_validado(cpf):
    conn = conectar_bd()
    cur = conn.cursor()

    query = "SELECT cpf FROM clientes WHERE cpf = %s"
    cur.execute(query, (cpf,))
    cpf_validado = cur.fetchall()

    cur.close()
    conn.close()

    return bool(cpf_validado)  # Verifica se a lista não está vazia


def email_validado(email):
    conn = conectar_bd()
    cur = conn.cursor()

    query = "SELECT email FROM clientes WHERE email = %s"
    cur.execute(query, (email,))
    email_validado = cur.fetchall()

    cur.close()
    conn.close()

    return bool(email_validado)  # Verifica se a lista não está vazia


def insert_customer(nome, cpf, email, telefone, data_nascimento, senha,
                    id_tipo_conta, id_status_conta):
    create_table()
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

                cpf = cpf.replace(" ", "").replace("-", "").replace("/", "")
                cpf_formatado = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

                telefone = telefone.replace(" ", "").replace("-", "").replace("/", "")
                telefone_formatado = f"({telefone[:2]}){telefone[2:7]}-{telefone[7:]}"

                data_nascimento = data_nascimento.replace(" ", "").replace("-", "").replace("/", "")
                data_nascimento_formatado = f"{data_nascimento[:2]}/{data_nascimento[2:4]}/{data_nascimento[4:]}"

                if nome and cpf_formatado and email and telefone_formatado and data_nascimento_formatado and senha:
                    def secret():
                        a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                            's','t','u', 'v', 'w', 'x', 'y', 'z']
                        b = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
                        c = list("!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")

                        alfa = []

                        for _ in range(200):
                            alfa.append(random.choice(a))
                            alfa.append(random.choice(b))
                            alfa.append(random.choice(c))

                        alfa = ''.join(map(str, alfa))
                        return alfa

                    def get_values_secret_max():
                        values_max = list(string.ascii_uppercase)
                        especial_characters = string.punctuation
                        values_max += especial_characters
                        random.shuffle(values_max)
                        max_secret = ''.join(map(str, values_max))
                        return max_secret

                    def get_values_secret_min():
                        values_min = list(string.ascii_lowercase)
                        especial_characters = string.punctuation
                        values_min += especial_characters
                        random.shuffle(values_min)
                        min_secret = ''.join(map(str, values_min))
                        return min_secret

                    alfa = secret()

                    def get_values_secrets():
                        choice_values_secrets = []

                        secret_min = list(min_secret)
                        secret_max = list(max_secret)
                        nome_secret = list(nome)
                        phone_secret = list(telefone_formatado)
                        password_secret = list(senha)
                        data_secret = list(data_nascimento_formatado)

                        password_index = 0
                        secret_max_index = 0
                        secret_min_index = 0
                        data_index = 0
                        nome_secret_index = 0
                        phone_secret_index = 0

                        for i in range(len(alfa)):
                            if i % 5 == 0 and nome_secret and nome_secret_index < len(nome_secret):
                                choice_values_secrets.append(nome_secret[nome_secret_index])
                                nome_secret_index += 1
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
                                choice_values_secrets.append(alfa[i])
                        return choice_values_secrets

                    max_secret = get_values_secret_max()
                    min_secret = get_values_secret_min()

                    salt = get_values_secrets()
                    password_secret = ''.join(map(str, salt)).replace(' ', '').replace('\n', '')

                    query_customers = """
                        INSERT INTO clientes (nome, cpf, email, telefone, data_nascimento, secret, id_tipo_conta, id_status_conta)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING id
                        """

                    query_secret_alfa = """
                        INSERT INTO secret_alfa (id_cliente, alfa)
                        VALUES (%s, %s)
                        """

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
                    )

                    cur.execute(query_customers, values_customer)
                    id_cliente = cur.fetchone()[0]

                    values_secret_alfa = (id_cliente, alfa)
                    values_secret_max = (id_cliente, max_secret)
                    values_secret_min = (id_cliente, min_secret)

                    cur.execute(query_secret_alfa, values_secret_alfa)
                    cur.execute(query_secret_max, values_secret_max)
                    cur.execute(query_secret_min, values_secret_min)

                    conn.commit()

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
