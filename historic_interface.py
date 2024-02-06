import flet as ft
from flet import *
from postgres_bd import conectar_bd
from psycopg2 import extras
from datetime import datetime

id_cliente = 1

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

def main(page: ft.Page):
    page.window_width = 600
    page.window_height = 620
    page.scroll = True

    historico_atual = get_historico_atual()

    historic_movement = []
    for tupla in historico_atual:
        for transacao in tupla:
            tipo = transacao['tipo']
            if  tipo == 'Depósito' or  tipo == 'Saque':
                valor = transacao['valor']
                date_ = transacao['data']
                hora_ = transacao['hora']
                historic_movement.append({'tipo':tipo,'valor': valor,'date': date_,'hora': hora_})

    show_historic = Row(
        [
            Text(
                "HISTÓRICO",
                weight='bold',
                size=70,
                color=colors.YELLOW_900
            ),
        ],
        alignment=MainAxisAlignment.CENTER
    )

    page.add(show_historic)
    
    for key_deposit in historic_movement:
        type_deposit = key_deposit['tipo']
        value_deposit = key_deposit['valor']
        date_deposit = key_deposit['date']
        hora_deposit = key_deposit['hora']

        show_transaction = Container(
            content=Column(
                [
                    Text(
                        f"{type_deposit} R${value_deposit}, Data {date_deposit} {hora_deposit}",
                        color=colors.GREEN if type_deposit == 'Depósito' else colors.RED,
                        text_align=MainAxisAlignment.CENTER,
                        size=25 if type_deposit == 'Depósito' else 27
                    )
                ],
            ),
        )

        page.add(Row(
            [
                show_transaction,
            ],
            alignment=MainAxisAlignment.SPACE_AROUND
        ))


ft.app(target=main)