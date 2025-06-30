import PySimpleGUI as sg
from exceptions.senha_incorreta_exception import SenhaIncorretaException
from exceptions.membro_nao_encontrado_exception import MembroNaoEncontradoException

class TelaLogin:
    def __init__(self, sistema):
        self.sistema = sistema

    def exibir(self):
        layout = [
            [sg.Text('LOGIN', font=('Arial', 16, 'bold'))],
            [sg.Text('')],
            [sg.Text('Nome:', size=(8, 1)), sg.Input(key='nome', size=(25, 1))],
            [sg.Text('Senha:', size=(8, 1)), sg.Input(key='senha', password_char='*', size=(25, 1))],
            [sg.Text('')],
            [sg.Button('Entrar', font=('Arial', 10)), sg.Button('Voltar', font=('Arial', 10))],
        ]

        window = sg.Window('Login', layout, element_justification='left')

        while True:
            event, values = window.read()

            if event in (sg.WIN_CLOSED, 'Voltar'):
                window.close()
                return None

            elif event == 'Entrar':
                if values['nome'] and values['senha']:
                    try:
                        sucesso, mensagem = self.sistema.fazer_login(values['nome'], values['senha'])
                        if sucesso:
                            membro_logado = self.sistema.membro_logado
                            sg.popup(mensagem, title='Login realizado')
                            window.close()
                            return membro_logado
                        else:
                            sg.popup_error(mensagem)

                    except SenhaIncorretaException as e:
                        sg.popup_error(f'Erro: {e.message}')
                    except MembroNaoEncontradoException as e:
                        sg.popup_error(f'Erro: {e.message}')
                    except Exception as e:
                        sg.popup_error(f'Erro no login: {str(e)}')
                else:
                    sg.popup_error('Digite nome e senha!')

        window.close()