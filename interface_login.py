import flet as ft
from flet import *
from flet_route import Params, Basket




LIGHT_SEED_COLOR = colors.DEEP_ORANGE  # cor para combinar com o tema(tema branco)
DARK_SEED_COLOR = colors.INDIGO  # cor para combinar com o tema(tema escuro)

def login(page: ft.Page, params=Params, basket=Basket):
    global login_value, password_value  # deixando as variveis global para ser usado fora da função sem precisar de colocar como retorno
    def check_item_clicked(e):
        e.control.checked = not e.control.checked # controle do click no appbar
        page.update()
    page.title = "Banco Silva" # titulo da pagina
    page.theme_mode = "dark" # tema da pagina
    page.window_resizable = False  # tamanho da janela fixo
    page.window_width = 900   # largura da janela
    page.window_height = 920 # altura da janel
    page.horizontal_alignment = MainAxisAlignment.CENTER  # alinhamento dos elementos na horizontal indicado para o centro
    page.theme = Theme(color_scheme_seed=LIGHT_SEED_COLOR, use_material3=True)  # temas
    page.dark_theme = Theme(color_scheme_seed=DARK_SEED_COLOR, use_material3=True) 
    page.scroll = True   # habilita a rolagem na pagina
    

    def toggle_theme_mode(e): # funçao para mudar o tema
        page.theme_mode = "dark" if page.theme_mode == "light" else "light" # si o tema da pagina for light, muda pra dark, e vise versa
        lightMode.icon = (
            icons.LIGHT_MODE_ROUNDED if page.theme_mode == "light" else icons.DARK_MODE_ROUNDED
        ) # icone muda de acordo com o tema
        page.update()

    lightMode = IconButton(
        icons.LIGHT_MODE_ROUNDED if page.theme_mode == "light" else icons.DARK_MODE_ROUNDED,
        on_click=toggle_theme_mode,
    ) # botao que altera o modo do tema também  chama a função toggle_theme_mode 
    
    page.padding = 50   # espacamento entre os componentes
    
    icon_login = Container(  # variavel icone login, container para controlar facilmente os componentes
        content=Row( # colocar o elementoi em linha, também facil de manipular doque coluna.
            [
                Icon( # elemento a ser tratado, é um icone
                    icons.PERSON, # icone a ser usado
                    size=350, #  tamanho do icone
                    color=colors.YELLOW_900 # cor do icone
                )
            ],
            alignment='center'  # centralizar os elementos
        ),
        visible=True # visibilidade do elemento na pagina
    ) 

    login_value = TextField( # variavel valor de login, usando textfield, pois assim consigo receber o valor digitado.
        label="LOGIN", #  texto para descrever o uqe é
        border_width=3,  # espessura da borda
        border_radius=50, # arredondamento dos cantos
        bgcolor=colors.WHITE12,  # cor do fundo
        border_color=colors.YELLOW_900,  # cor da borda
        color=colors.YELLOW_900,   # cor do texto
        selection_color=colors.BLUE_GREY_200,   # cor quando selecionado
    )
    login_textfield = Container( # variavel para tratar melhor o login, pois fica facilmente manivel
        content=Row(
            [
                login_value # chamada  a variavel criada anteriormente
            ],
            alignment='center'
        ),
        padding=15,
        visible=True
    )

    password_value = TextField(
        label="SENHA",
        border_width=3,
        border_radius=50,
        bgcolor=colors.WHITE12,
        border_color=colors.YELLOW_900,
        color=colors.YELLOW_900,
        selection_color=colors.BLUE_GREY_200,
        password=True, # senha em vez de texto normal
        can_reveal_password=True, # icone de um olho  que mostra ou esconde a senha
    )
    password_textfield = Container(
        content=Row(
            [
                password_value
            ],
            alignment='center',
        ),
        padding=20,
        visible=True
    )

    login_button = Container(
        content=Row( # a linha com duas variaveis, quando utilizadas mostra os elementos um do lado do outro
            [
                IconButton( #  botão com icone
                    icon_size=150,
                    on_click=lambda _: page.go("/user"),  # redireciona pra pagina user quando clicado, usando o flet_router mensionado antes
                    icon=icons.LOGIN_ROUNDED,
                    tooltip="ENTRAR", #  dica do botao, aparece quando passa o mouse em cima do icone
                    icon_color=colors.YELLOW_900
                ),

                IconButton(
                    icon_size=150,
                    on_click=lambda _: page.go("/register"),
                    icon=icons.HOW_TO_REG_ROUNDED,
                    tooltip="CADASTRAR",
                    icon_color=colors.YELLOW_900
                )
            ],
            alignment="center",
            spacing=200 # da espaço entre os elementos na linha
        ),
        visible=True,
        top=80, right=180 # usando para manipular o local que quero que fique os elementos, não esqueça! tem que utilizar quando ira adicionar a pagina, usando alguma parametro, para essa visualização utilize stack(variavel aqui)
        )
    
    login_appbar = AppBar( # app bar e a barra que fica  no topo da tela
        toolbar_height=50, # altura da barra
        bgcolor=colors.SECONDARY_CONTAINER,
        leading=Icon(icons.ACCOUNT_BALANCE_ROUNDED),  # icone do menu de navegação
        leading_width=40,
        title=Text("BANCO SILVA", weight='bold', size=25),  # titulo da pagina
        center_title=True,    # centraliza o titulo
        actions=[ # açoes no app bar
            PopupMenuButton( #  botao para abrir um menu pop up
                lightMode, # chamada da variavel de mudar o tema
                tooltip='TEMA'
                ),
            PopupMenuButton(
                IconButton(
                    icon=icons.PERSON_ROUNDED,
                    on_click=lambda _:page.go("/login"),
                ),
                tooltip='LOGIN'
            ),
        ]
    )
    
    page.update()

    return View( #  cria a view com todos os componentes criados acima, para mostrar quando utilizo o flet_route
        "/login", # nome da chamada, para em outra pagina si colocar uma ação colocando esse nome, faz essa chamada aqui.
        controls=[
            login_appbar, icon_login, login_textfield, password_textfield, Stack([login_button]) # com a chamada feita, essa parte coloca os elementos na tela, lembrando de utilizar p stack(), caso for precisar de ajustar melhor o elemnto na tela
        ]
    )

def to_values_login(): # uma função criada para ser usada em outras paginas, para ser feito um tratamento nos dados para verificar o usuario no banco de dados
    login = login_value.value #  pega o valor digitado no campo de usuario
    password = password_value.value  # pega o valor digitado no campo de senha
    return login, password # retorna esses valores para ser usado em qualquer funcao que chamar esse callback
