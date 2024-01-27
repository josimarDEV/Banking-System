from postgres_bd import conectar_bd


def validate_password(email, senha):
    print(senha)

    def get_secret_client(email):
        conn = conectar_bd()
        cur = conn.cursor()

        try:
            query = "SELECT secret FROM clientes WHERE email = %s"
            cur.execute(query, (email,))
            password = cur.fetchone()
            if password:
                return ''.join(map(str, password[0]))
        except Exception as e:
            print(f"Erro ao obter secret do cliente: {e}")
        finally:
            cur.close()
            conn.close()

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

    def get_name(email):
        conn = conectar_bd()
        cur = conn.cursor()

        try:
            query = "SELECT nome FROM clientes WHERE email = %s"
            cur.execute(query, (email,))
            nome = cur.fetchall()
            if nome:
                return ''.join(map(str, nome[0]))
        except Exception as e:
            print(f"Erro ao obter o nome: {e}")
        finally:
            cur.close()
            conn.close()

    def get_telefone(email):
        conn = conectar_bd()
        cur = conn.cursor()

        try:
            query = "SELECT telefone FROM clientes WHERE email = %s"
            cur.execute(query, (email,))
            telefone_formatado = cur.fetchall()
            if telefone_formatado:
                return ''.join(map(str, telefone_formatado[0]))
        except Exception as e:
            print(f"Erro ao obter o telefone: {e}")
        finally:
            cur.close()
            conn.close()

    def get_data_nascimento(email):
        conn = conectar_bd()
        cur = conn.cursor()

        try:
            query = "SELECT data_nascimento FROM clientes WHERE email = %s"
            cur.execute(query, (email,))
            data_nascimento = cur.fetchall()
            if data_nascimento:
                return ''.join(map(str, data_nascimento[0]))
        except Exception as e:
            print(f"Erro ao obter data nascimento: {e}")
        finally:
            cur.close()
            conn.close()

    def get_secret_alfa(id_cliente):
        conn = conectar_bd()
        cur = conn.cursor()

        try:
            query = "SELECT alfa FROM secret_alfa WHERE id_cliente = %s"
            cur.execute(query, (id_cliente,))
            secret_alfa = cur.fetchall()
            if secret_alfa:
                return ''.join(map(str, secret_alfa[0]))
        except Exception as e:
            print(f"Erro ao obter alfa: {e}")
        finally:
            cur.close()
            conn.close()

    def get_max_secret(id_cliente):
        conn = conectar_bd()
        cur = conn.cursor()

        try:
            query = "SELECT max_alfa FROM max_secret WHERE id_cliente = %s"
            cur.execute(query, (id_cliente,))
            max_secret = cur.fetchall()
            if max_secret:
                return ''.join(map(str, max_secret[0]))
        except Exception as e:
            print(f"Erro ao obter alfa: {e}")
        finally:
            cur.close()
            conn.close()

    def get_min_secret(id_cliente):
        conn = conectar_bd()
        cur = conn.cursor()

        try:
            query = "SELECT min_alfa FROM min_secret WHERE id_cliente = %s"
            cur.execute(query, (id_cliente,))
            min_secret = cur.fetchall()
            if min_secret:
                return ''.join(map(str, min_secret[0]))
        except Exception as e:
            print(f"Erro ao obter alfa: {e}")
        finally:
            cur.close()
            conn.close()

    password = get_secret_client(email)
    if password:
        def get_values_secrets(nome, telefone_formatado, senha, alfa, max_secret, min_secret,
                               data_nascimento_formatado):
            choice_values_secrets = []

            secret_min = list(min_secret)
            secret_max = list(max_secret)
            nome_secret = list(nome)
            phone_secret = list(telefone_formatado)
            password_secret = list(senha)
            data_secret = list(data_nascimento_formatado)
            print(password_secret)

            password_index = 0
            secret_max_index = 0
            secret_min_index = 0
            data_index = 0
            phone_secret_index = 0
            nome_secret_index = 0

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

        id_cliente = get_id_client(email)
        nome = get_name(email)
        telefone_formatado = get_telefone(email)
        data_nascimento_formatado = get_data_nascimento(email)
        alfa = get_secret_alfa(id_cliente)
        max_secret = get_max_secret(id_cliente)
        min_secret = get_min_secret(id_cliente)
        salt = get_values_secrets(nome, telefone_formatado, senha, alfa, max_secret, min_secret,
                                  data_nascimento_formatado)
        secret = ''.join(map(str, salt)).replace(' ', '').replace('\n', '')

        if password == secret:
            print(password)
            print()
            print(secret)
            return 'Senha válida!'
        else:
            return 'Senha inválida!'
    else:
        return 'Email não encontrado.'
