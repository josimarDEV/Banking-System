from postgres_bd import conectar_bd


def create_savings(email):
    conn = conectar_bd()
    cur = conn.cursor()

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

    def get_id_type_conta(email):
        conn = conectar_bd()
        cur = conn.cursor()

        try:
            query = "SELECT id_tipo_conta FROM clientes WHERE email = %s"
            cur.execute(query, (email,))
            id_tipo_conta = cur.fetchone()
            if id_tipo_conta:
                return id_tipo_conta[0]
        except Exception as e:
            print(f"Erro ao obter tipo de conta: {e}")
        finally:
            cur.close()
            conn.close()

    def get_id_stats_account(email):
        conn = conectar_bd()
        cur = conn.cursor()

        try:
            query = "SELECT id_status_conta FROM clientes WHERE email = %s"
            cur.execute(query, (email,))
            id_status_conta = cur.fetchone()
            if id_status_conta:
                return id_status_conta[0]
        except Exception as e:
            print(f"Erro ao obter  status da conta:{e}")
        finally:
            cur.close()
            conn.close()

    if get_id_stats_account(email) == 1:
        id_status_conta = "ATIVA"
    elif get_id_stats_account(email) == 2:
        id_status_conta = "INATIVA"
    else:
        id_status_conta = "BLOQUEADA"

    if get_id_type_conta(email) == 1:
        id_tipo_conta = "CONTA POUPANÇA"
    elif get_id_type_conta(email) == 2:
        id_tipo_conta = "CONTA CORRENTE"
    else:
        id_tipo_conta = "CONTA ESPECIAL"

    id_cliente = get_id_client(email)

    def id_cliente_validado(id_cliente):
        conn = conectar_bd()
        cur = conn.cursor()

        query = "SELECT id_cliente FROM conta_poupanca WHERE id_cliente = %s"
        cur.execute(query, (id_cliente,))
        id_cliente_validado = cur.fetchall()

        cur.close()
        conn.close()

        return bool(id_cliente_validado)  # Verifica se a lista não está vazia
    if not  id_cliente_validado(id_cliente):
        try:
            query = """
            INSERT INTO conta_poupanca (id_cliente, numero_banco, agencia_poupanca, saldo, tipo_conta, status_conta)
            VALUES (%s, %s, %s, %s, %s, %s);
            """

            savings_values = (
                id_cliente, "194", "1994", 0, id_tipo_conta, id_status_conta
            )

            cur.execute(query, savings_values)

            conn.commit()

            print("conta poupança criada com sucesso")
        except Exception as e:
            print(f"Erro na inserção conta poupança: {e}")
        finally:
            cur.close()
            conn.close()
    else:
        print("Cliente já possui uma conta popança")
