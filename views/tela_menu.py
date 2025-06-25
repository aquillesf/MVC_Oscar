import PySimpleGUI as sg

class TelaMenu:
    def __init__(self, sistema, membro_logado):
        self.sistema = sistema
        self.membro_logado = membro_logado

    def exibir(self):
        from .tela_principal import TelaPrincipal
        
        permissoes = self.sistema.obter_permissoes_usuario()
        opcoes_registrador = []
        opcoes_votador = []

        if permissoes['pode_registrar']:
            opcoes_registrador = [
                [sg.Button('Adicionar Filme', size=(20, 2), font=('Arial', 10))],
                [sg.Button('Adicionar Ator/Atriz', size=(20, 2), font=('Arial', 10))],
                [sg.Button('Adicionar Indicação', size=(20, 2), font=('Arial', 10))],
                [sg.Button('Deletar Filme', size=(20, 2), font=('Arial', 10), button_color=('white', 'darkred'))],
                [sg.Button('Deletar Ator/Atriz', size=(20, 2), font=('Arial', 10), button_color=('white', 'darkred'))],
                [sg.Button('Deletar Indicação', size=(20, 2), font=('Arial', 10), button_color=('white', 'darkred'))],
            ]

        if permissoes['pode_votar']:
            opcoes_votador = [
                [sg.Button('Votar em Categoria', size=(20, 2), font=('Arial', 10))],
            ]

        layout = [
            [sg.Text(f'Bem-vindo, {permissoes["nome"]} ({permissoes["tipo"]})',
                     font=('Arial', 14, 'bold'))],
            [sg.Text('')],
        ] + opcoes_registrador + opcoes_votador + [
            [sg.Button('Gerar Relatório', size=(20, 2), font=('Arial', 10))],
            [sg.Button('Alterar Senha', size=(20, 2), font=('Arial', 10))],
            [sg.Button('Logout', size=(20, 2), font=('Arial', 10))],
        ]

        window = sg.Window('Menu Principal', layout, element_justification='center')
        
        tela_principal = TelaPrincipal()
        tela_principal.sistema = self.sistema
        tela_principal.membro_logado = self.membro_logado

        while True:
            event, values = window.read()

            if event in (sg.WIN_CLOSED, 'Logout'):
                self.sistema.fazer_logout()
                self.membro_logado = None
                window.close()
                break

            elif event == 'Adicionar Filme':
                window.close()
                resultado = tela_principal.tela_adicionar_filme()
                if resultado:
                    self.exibir()
                break

            elif event == 'Alterar Senha':
                window.close()
                resultado = tela_principal.tela_alterar_senha()
                if resultado:
                    self.exibir()
                break

            elif event == 'Adicionar Ator/Atriz':
                window.close()
                resultado = tela_principal.tela_adicionar_ator()
                if resultado:
                    self.exibir()
                break

            elif event == 'Adicionar Indicação':
                window.close()
                resultado = tela_principal.tela_adicionar_indicacao()
                if resultado:
                    self.exibir()
                break

            elif event == 'Votar em Categoria':
                window.close()
                resultado = tela_principal.tela_votar()
                if resultado:
                    self.exibir()
                break

            elif event == 'Deletar Filme':
                window.close()
                resultado = tela_principal.tela_deletar_filme()
                if resultado:
                    self.exibir()
                break

            elif event == 'Deletar Ator/Atriz':
                window.close()
                resultado = tela_principal.tela_deletar_ator()
                if resultado:
                    self.exibir()
                break

            elif event == 'Deletar Indicação':
                window.close()
                resultado = tela_principal.tela_deletar_indicacao()
                if resultado:
                    self.exibir()
                break

            elif event == 'Gerar Relatório':
                tela_principal.mostrar_relatorio()

        window.close()
