import psycopg2


def conectar_bd():
    db_name = "sistema bancario"
    user = "josimar_504"
    password = "941402"
    host = "localhost"
    port = "5432"

    conn = psycopg2.connect(dbname=db_name, user=user, password=password, host=host, port=port)
    return conn
