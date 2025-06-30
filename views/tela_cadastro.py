import PySimpleGUI as sg
from exceptions.membro_ja_existente_exception import MembroJaExistenteException
from exceptions.dados_invalidos_exception import DadosInvalidosException

class TelaCadastro:
    def __init__(self, sistema):
        self.sistema = sistema

    def exibir(self):
        layout = [
            [sg.Text('CADASTRO DE MEMBRO', font=('Arial', 16, 'bold'))],
            [sg.Text('')],
            [sg.Text('Nome:', size=(10, 1)), sg.Input(key='nome', size=(25, 1))],
            [sg.Text('Senha:', size=(10, 1)), sg.Input(key='senha', password_char='*', size=(25, 1))],
            [sg.Text('Tipo:', size=(10, 1)), sg.Combo(['VOTADOR', 'REGISTRADOR'], key='tipo', size=(23, 1))],
            [sg.Text('')],
            [sg.Button('Cadastrar', font=('Arial', 10)), sg.Button('Voltar', font=('Arial', 10))],
        ]

        window = sg.Window('Cadastro', layout, element_justification='left')

        while True:
            event, values = window.read()

            if event in (sg.WIN_CLOSED, 'Voltar'):
                window.close()
                return True

            elif event == 'Cadastrar':
                if values['nome'] and values['senha'] and values['tipo']:
                    try:
                        sucesso, mensagem = self.sistema.cadastrar_membro(
                            values['nome'], values['tipo'], values['senha']
                        )

                        if sucesso:
                            sg.popup(mensagem, title='Sucesso')
                            window.close()
                            return True
                        else:
                            sg.popup_error(mensagem)

                    except MembroJaExistenteException as e:
                        sg.popup_error(f'Erro: {e.message}')
                    except DadosInvalidosException as e:
                        sg.popup_error(f'Dados inválidos: {e.message}')
                    except Exception as e:
                        sg.popup_error(f'Erro ao cadastrar membro: {str(e)}')
                else:
                    sg.popup_error('Preencha todos os campos!')
                    
        window.close()