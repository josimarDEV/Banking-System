# será implementado na interface do usuário
#     PopupMenuButton(
        #         items=[
        #             PopupMenuItem(text="PERFIL", icon=icons.ACCOUNT_BOX_ROUNDED),
        #             PopupMenuItem(icon=icons.CREDIT_CARD, text="CARTÃO"),
        #             PopupMenuItem(
        #                 content=Row(
        #                     [
        #                         Icon(icons.HOURGLASS_TOP_OUTLINED),
        #                         Text("Item with a custom content"),
        #                     ]
        #                 ),
        #                 on_click=lambda _: print(
        #                     "Button with a custom content clicked!"
        #                 ),
        #             ),
        #             PopupMenuItem(),  # divider
        #             PopupMenuItem(
        #                 text="Checked item", checked=False, on_click=check_item_clicked
        #             ),
        #         ],
        #         tooltip='MENU'
        #     ),