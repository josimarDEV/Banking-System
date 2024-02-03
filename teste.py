from postgres_bd import conectar_bd

def client_balance(id_cliente):
    conn = conectar_bd()
    cur = conn.cursor()
    
    try:
        query = "SELECT saldo FROM conta_poupanca WHERE id_cliente = %s"
        cur.execute(query, (id_cliente,))
        balance = cur.fetchone()  # Usando fetchone() para obter apenas uma linha (se existir)
        
        if balance:
            return balance[0]  # Retorna o saldo da conta poupança
        else:
            return None  # Retorna None se o cliente não tiver uma conta poupança
    except Exception as e:
        print(f"Erro na consulta de saldo da conta poupança: {e}")
    finally:
        cur.close()
        conn.close()

# Exemplo de uso
id_cliente = 1
saldo = client_balance(id_cliente)

if saldo is not None:
    print(f"O saldo da conta poupança do cliente {id_cliente} é: {saldo}")
else:
    print(f"O cliente {id_cliente} não possui uma conta poupança.")
