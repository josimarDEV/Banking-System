# Main o script que define as funçoes para realizar a rota das paginas utilizadas
import flet as ft # Importa a biblioteca de interface flet e muda simplifica seu nome para ft
from flet import * # Importa todos os modulos da classes, sem precisar de chamar ft antes exemplo: ft.Texto
from flet_route import Routing, path   #Importa as funcões do routing, e path, da biblioteca flet_route que vamos utilizar para fazer nossa rotas entre paginas
from interface_home import home #  Importa a interface home
from interface_login import login #  Importa a interface login
from interface_register import register #  Importa a interface registro
from interface_user import user_interface #  Importa a interface usuario
from interface_historic import view_historic #  Importa a interface historico


def main(page: ft.Page): # Cria a função main, que recebe como parametro a página atual
    # Chama as interfaces criadas
    page.scroll = True # a pagina pode ter a rolagem ativada caso as linhas ultrapasse m a area visivel na tela
    app_routes = [
        path(url="/", clear=True, view=home), # define o nome da url para ser chamado,  limpa a tela anterior, a pagina a ser visualizada
        path(url="/login", clear=True, view=login),
        path(url="/register", clear=True, view=register),
        path(url="/user", clear=True, view=user_interface),
        path(url="/user_validado", clear=True, view=user_interface),
        path(url="/historic", clear=True, view=view_historic)
    ] # Define uma lista com todas as rotas do programa

    Routing(
        page=page,app_routes=app_routes
        ) #  Faz o tratamento de requisições e  chamada das views correspondentes

    page.go(page.route)  # Abre a página definida na variavel "route"
    page.update()        # Atualiza a página aberta

ft.app(target=main)    # Inicia o aplicativo com a função main como alvo