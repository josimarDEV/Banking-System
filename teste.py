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

    historic_deposit = []
    historic_withdraw = []
    for tupla in historico_atual:
        for transacao in tupla:
            tipo = transacao['tipo']
            if  tipo == 'Depósito':
                valor = transacao['valor']
                date_ = transacao['data']
                hora_ = transacao['hora']
                historic_deposit.append({'tipo':tipo,'valor': valor,'date': date_,'hora': hora_})
            elif tipo == 'Saque':
                valor = transacao['valor']
                date_ = transacao['data']
                hora_ = transacao['hora']
                historic_withdraw.append({'tipo':tipo,'valor': valor,'date': date_,'hora': hora_})

    print(historic_deposit)
    print()
    print(historic_withdraw)
    show_historic = Row(
        [
            Text(
                "HISTÓRICO",
                weight='bold',
                size=50,
                color=colors.YELLOW_900
            ),
        ],
        alignment=MainAxisAlignment.CENTER
    )

    page.add(show_historic)
    
    for key_deposit in historic_deposit:
        type_deposit = key_deposit['tipo']
        value_deposit = key_deposit['valor']
        date_deposit = key_deposit['date']
        hora_deposit = key_deposit['hora']
        
        show_deposit = Container(
                    content=Column(
                        [
                            Text(
                                f"{type_deposit}  R${value_deposit} Data{date_deposit} {hora_deposit}",
                                color=colors.GREEN
                            )
                        ],
                        
                    ),
                )
        
        page.add(Row(
        [
            show_deposit,
        ],
        alignment=MainAxisAlignment.SPACE_AROUND
        ))
    
    for key_withdraw in historic_withdraw:
        type_withdraw = key_withdraw['tipo']
        value_withdraw = key_withdraw['valor']
        date_withdraw = key_withdraw['date']
        hora_withdraw = key_withdraw['hora']
        
        show_withdraw = Container(
            content=Column(
                [
                    Text(
                        f"{type_withdraw}   R${value_withdraw} Data{date_withdraw} hora:{hora_withdraw}",
                        color=colors.RED
                    )
                ],
                
            ),
        )
        page.add(Row(
        [
            show_withdraw,
        ],
        alignment=MainAxisAlignment.SPACE_AROUND
        ))

ft.app(target=main)