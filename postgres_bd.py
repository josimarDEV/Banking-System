import psycopg2  # Importa o módulo do PostgreSQL


def conectar_bd(): # Função que faz a conexão com o banco de dados PostgreSQL
    db_name = "sistema bancario"                       # Nome do Banco de Dados
    user = "josimar_504"                               # Usuário do BD
    password = "941402"                                 # Senha do usuário
    host = "localhost"                                   # Endereço do servidor
    port = "5432"                                            # Porta para acesso ao DBMS (PostgreSQL)

    conn = psycopg2.connect(dbname=db_name, user=user, password=password, host=host, port=port) # Faz a conexão com o Banco de dados com conn como variavel  e depois de = seu atributos para essa conexão
    return conn #  Retorna a conexão com o banco de dados
