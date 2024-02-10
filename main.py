# Main
import flet as ft
from flet import *
from flet_route import Routing, path
from interface_home import home
from interface_login import login
from interface_register import register
from interface_user import user_interface
from interface_historic import view_historic


def main(page: ft.Page):
    # Chama as interfaces criadas
    app_routes = [
        path(url="/", clear=True, view=home),
        path(url="/login", clear=True, view=login),
        path(url="/register", clear=True, view=register),
        path(url="/user", clear=True, view=user_interface),
        path(url="/user_validado", clear=True, view=user_interface),
        path(url="/historic", clear=True, view=view_historic)
    ]

    Routing(
        page=page,app_routes=app_routes
        )

    page.go(page.route)
    page.update()

ft.app(target=main)