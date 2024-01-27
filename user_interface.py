import flet as ft
from flet import *


def user_interface(page: ft.Page):
    page.window_width = 600
    page.window_height = 620


ft.app(target=user_interface)
