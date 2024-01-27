from postgres_bd import conectar_bd


def create_table():
    conn = conectar_bd()
    cur = conn.cursor()

    try:
        script_path = "console.sql"
        with open(script_path, "r") as file:
            sql_script = file.read()

        cur.execute(sql_script)
        conn.commit()

        return "Tabelas criadas com sucesso!"
    except Exception as e:
        conn.rollback()
        return f"Erro ao criar tabelas: {e}"
    finally:
        cur.close()
        conn.close()
