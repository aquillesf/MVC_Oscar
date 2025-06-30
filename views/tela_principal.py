import PySimpleGUI as sg
from exceptions.oscar_exception import OscarException
from exceptions.membro_ja_existente_exception import MembroJaExistenteException
from exceptions.membro_nao_encontrado_exception import MembroNaoEncontradoException
from exceptions.senha_incorreta_exception import SenhaIncorretaException
from exceptions.permissao_negada_exception import PermissaoNegadaException
from exceptions.item_nao_encontrado_exception import ItemNaoEncontradoException
from exceptions.voto_ja_realizado_exception import VotoJaRealizadoException
from exceptions.dados_invalidos_exception import DadosInvalidosException
from exceptions.arquivo_exception import ArquivoException
from controllers.sistema_oscar_controller import SistemaOscarController
from .tela_cadastro import TelaCadastro
from .tela_login import TelaLogin
from .tela_menu import TelaMenu

class TelaPrincipal:
    def __init__(self):
        self.sistema = SistemaOscarController()
        self.membro_logado = None
        sg.theme('DarkBlue3')

    def tela_principal(self):
        layout = [
            [sg.Text('SISTEMA DO OSCAR', font=('Arial', 20, 'bold'), justification='center')],
            [sg.Text('')],
            [sg.Button('Cadastrar-se', size=(15, 2), font=('Arial', 12))],
            [sg.Button('Login', size=(15, 2), font=('Arial', 12))],
            [sg.Button('Sair', size=(15, 2), font=('Arial', 12))],
        ]

        window = sg.Window('Sistema Oscar', layout, element_justification='center', size=(300, 250))

        while True:
            event, values = window.read()

            if event in (sg.WIN_CLOSED, 'Sair'):
                break
            elif event == 'Cadastrar-se':
                window.close()
                tela_cadastro = TelaCadastro(self.sistema)
                resultado = tela_cadastro.exibir()
                if resultado:
                    self.tela_principal()
                break
            elif event == 'Login':
                window.close()
                tela_login = TelaLogin(self.sistema)
                membro_logado = tela_login.exibir()
                if membro_logado:
                    self.membro_logado = membro_logado
                    tela_menu = TelaMenu(self.sistema, self.membro_logado)
                    tela_menu.exibir()
                    self.tela_principal()
                else:
                    self.tela_principal()
                break

        window.close()

    def tela_alterar_senha(self):
        layout = [
            [sg.Text('ALTERAR SENHA', font=('Arial', 16, 'bold'))],
            [sg.Text('')],
            [sg.Text('Senha Atual:', size=(12, 1)), sg.Input(key='senha_atual', password_char='*', size=(25, 1))],
            [sg.Text('Nova Senha:', size=(12, 1)), sg.Input(key='nova_senha', password_char='*', size=(25, 1))],
            [sg.Text('Confirmar:', size=(12, 1)), sg.Input(key='confirmar_senha', password_char='*', size=(25, 1))],
            [sg.Text('')],
            [sg.Button('Alterar', font=('Arial', 10)), sg.Button('Voltar', font=('Arial', 10))],
        ]

        window = sg.Window('Alterar Senha', layout, element_justification='left', finalize=True)

        while True:
            event, values = window.read()

            if event in (sg.WIN_CLOSED, 'Voltar'):
                window.close()
                return True

            elif event == 'Alterar':
                if values['senha_atual'] and values['nova_senha'] and values['confirmar_senha']:
                    if values['nova_senha'] != values['confirmar_senha']:
                        sg.popup_error('Nova senha e confirmação não coincidem!')
                        continue

                    try:
                        sucesso, mensagem = self.sistema.alterar_senha(
                            values['senha_atual'], values['nova_senha']
                        )

                        if sucesso:
                            sg.popup(mensagem, title='Sucesso')
                            window.close()
                            return True
                        else:
                            sg.popup_error(mensagem)

                    except SenhaIncorretaException as e:
                        sg.popup_error(f'Erro: {e.message}')
                    except DadosInvalidosException as e:
                        sg.popup_error(f'Erro: {e.message}')
                    except Exception as e:
                        sg.popup_error(f'Erro ao alterar senha: {str(e)}')
                else:
                    sg.popup_error('Preencha todos os campos!')

        window.close()

    def tela_adicionar_filme(self):
        layout = [
            [sg.Text('ADICIONAR FILME', font=('Arial', 16, 'bold'))],
            [sg.Text('')],
            [sg.Text('Título:', size=(12, 1)), sg.Input(key='titulo', size=(30, 1))],
            [sg.Text('Ano:', size=(12, 1)), sg.Input(key='ano', size=(30, 1))],
            [sg.Text('Gênero:', size=(12, 1)), sg.Input(key='genero', size=(30, 1))],
            [sg.Text('Diretor:', size=(12, 1)), sg.Input(key='diretor', size=(30, 1))],
            [sg.Text('Descrição:', size=(12, 1)), sg.Multiline(key='descricao', size=(30, 4))],
            [sg.Text('')],
            [sg.Button('Adicionar', font=('Arial', 10)), sg.Button('Voltar', font=('Arial', 10))],
        ]

        window = sg.Window('Adicionar Filme', layout)

        while True:
            event, values = window.read()

            if event in (sg.WIN_CLOSED, 'Voltar'):
                window.close()
                return True

            elif event == 'Adicionar':
                if all([values['titulo'], values['ano'], values['genero'], values['diretor']]):
                    try:
                        ano = int(values['ano'])
                        filme = self.sistema.filme_controller.criar_filme(
                            values['titulo'], ano, values['genero'],
                            values['diretor'], values['descricao']
                        )

                        sg.popup(f'Filme "{values["titulo"]}" adicionado com sucesso!', title='Sucesso')
                        window.close()
                        return True

                    except ValueError:
                        sg.popup_error('Ano deve ser um número válido!')
                    except DadosInvalidosException as e:
                        sg.popup_error(f'Dados inválidos: {e.message}')
                    except PermissaoNegadaException as e:
                        sg.popup_error(f'Erro: {e.message}')
                    except Exception as e:
                        sg.popup_error(f'Erro ao adicionar filme: {str(e)}')
                else:
                    sg.popup_error('Preencha todos os campos obrigatórios!')

        window.close()

    def tela_adicionar_ator(self): 
        layout = [
            [sg.Text('ADICIONAR ATOR/ATRIZ', font=('Arial', 16, 'bold'))],
            [sg.Text('')],
            [sg.Text('Nome:', size=(15, 1)), sg.Input(key='nome', size=(30, 1))],
            [sg.Text('Idade:', size=(15, 1)), sg.Input(key='idade', size=(30, 1))],
            [sg.Text('Nacionalidade:', size=(15, 1)), sg.Input(key='nacionalidade', size=(30, 1))],
            [sg.Text('Filmes (vírgula):', size=(15, 1)), sg.Input(key='filmes', size=(30, 1))],
            [sg.Text('Tipo:', size=(15, 1)), sg.Combo(['protagonista', 'coadjuvante'], key='tipo', size=(28, 1))],
            [sg.Text('')],
            [sg.Button('Adicionar', font=('Arial', 10)), sg.Button('Voltar', font=('Arial', 10))],
        ]

        window = sg.Window('Adicionar Ator/Atriz', layout)

        while True:
            event, values = window.read()

            if event in (sg.WIN_CLOSED, 'Voltar'):
                window.close()
                return True

            elif event == 'Adicionar':
                if all([values['nome'], values['idade'], values['nacionalidade'],
                        values['filmes'], values['tipo']]):
                    try:
                        idade = int(values['idade'])
                        filmes = [f.strip() for f in values['filmes'].split(',')]
                        ator = self.sistema.ator_controller.criar_ator(
                            values['nome'], idade, filmes,
                            values['tipo'], values['nacionalidade']
                        )

                        sg.popup(f'Ator/Atriz "{values["nome"]}" adicionado com sucesso!', title='Sucesso')
                        window.close()
                        return True

                    except ValueError:
                        sg.popup_error('Idade deve ser um número!')
                    except DadosInvalidosException as e:
                        sg.popup_error(f'Dados inválidos: {e.message}')
                    except PermissaoNegadaException as e:
                        sg.popup_error(f'Erro: {e.message}')
                    except Exception as e:
                        sg.popup_error(f'Erro ao adicionar ator: {str(e)}')
                else:
                    sg.popup_error('Preencha todos os campos!')

        window.close()

    def tela_adicionar_indicacao(self):
        categorias = self.sistema.categoria_controller.listar_categorias()
        if not categorias:
            sg.popup('Nenhuma categoria disponível!', title='Aviso')
            return True

        categorias_nomes = [cat.nome for cat in categorias]
        layout_categoria = [
            [sg.Text('ADICIONAR INDICAÇÃO', font=('Arial', 16, 'bold'))],
            [sg.Text('')],
            [sg.Text('Selecione a categoria:')],
            [sg.Listbox(categorias_nomes, size=(40, 10), key='categoria')],
            [sg.Text('')],
            [sg.Button('Próximo', font=('Arial', 10)), sg.Button('Voltar', font=('Arial', 10))],
        ]

        window = sg.Window('Selecionar Categoria', layout_categoria)
        categoria_selecionada = None

        while True:
            event, values = window.read()

            if event in (sg.WIN_CLOSED, 'Voltar'):
                window.close()
                return True

            elif event == 'Próximo':
                if values['categoria']:
                    categoria_nome = values['categoria'][0]
                    categoria_selecionada = self.sistema.categoria_controller.buscar_categoria(categoria_nome)
                    if categoria_selecionada:
                        break
                else:
                    sg.popup_error('Selecione uma categoria!')

        window.close()

        indicados = []
        if "Filme" in categoria_selecionada.nome:
            filmes = self.sistema.filme_controller.listar_filmes()
            indicados = [f"{filme.titulo} ({filme.ano})" for filme in filmes]
        elif "Diretor" in categoria_selecionada.nome:
            diretores = self.sistema.diretor_controller.listar_diretores()
            indicados = [diretor.nome for diretor in diretores]
        else:  
            atores = self.sistema.ator_controller.listar_atores()
            indicados = [f"{ator.nome} ({ator.tipo_ator})" for ator in atores]

        if not indicados:
            sg.popup_error('Não há itens disponíveis para esta categoria!')
            return True

        layout_indicado = [
            [sg.Text(f'CATEGORIA: {categoria_selecionada.nome}', font=('Arial', 14, 'bold'))],
            [sg.Text('')],
            [sg.Text('Selecione o indicado:')],
            [sg.Listbox(indicados, size=(50, 10), key='indicado')],
            [sg.Text('')],
            [sg.Button('Adicionar', font=('Arial', 10)), sg.Button('Voltar', font=('Arial', 10))],
        ]

        window = sg.Window('Selecionar Indicado', layout_indicado)

        while True:
            event, values = window.read()

            if event in (sg.WIN_CLOSED, 'Voltar'):
                window.close()
                return True

            elif event == 'Adicionar':
                if values['indicado']:
                    indicado_str = values['indicado'][0]
                    
                    if "Filme" in categoria_selecionada.nome:
                        titulo = indicado_str.split(' (')[0]
                        filme = self.sistema.filme_controller.buscar_filme(titulo)
                        indicado = filme
                    elif "Diretor" in categoria_selecionada.nome:
                        diretor = self.sistema.diretor_controller.buscar_diretor(indicado_str)
                        indicado = diretor
                    else:  
                        nome = indicado_str.split(' (')[0]
                        ator = self.sistema.ator_controller.buscar_ator(nome)
                        indicado = ator

                    try:
                        indicacao = self.sistema.indicacao_controller.criar_indicacao(
                            categoria_selecionada.nome, indicado
                        )

                        if indicacao:
                            sg.popup(f'Indicação adicionada com sucesso!', title='Sucesso')
                        else:
                            sg.popup_error('Erro ao adicionar indicação!')

                        window.close()
                        return True

                    except DadosInvalidosException as e:
                        sg.popup_error(f'Dados inválidos: {str(e)}')
                    except ItemNaoEncontradoException as e:
                        sg.popup_error(f'Item não encontrado: {str(e)}')
                    except Exception as e:
                        sg.popup_error(f'Erro ao adicionar indicação: {str(e)}')
                else:
                    sg.popup_error('Selecione um indicado!')

        window.close()

    def tela_votar(self):
        categorias = self.sistema.categoria_controller.listar_categorias()
        categorias_com_indicados = [cat for cat in categorias if cat.indicados]

        if not categorias_com_indicados:
            sg.popup('Nenhuma categoria com indicados disponível para votação!', title='Aviso')
            return True

        categorias_nomes = [cat.nome for cat in categorias_com_indicados]
        layout_categoria = [
            [sg.Text('VOTAR EM CATEGORIA', font=('Arial', 16, 'bold'))],
            [sg.Text('')],
            [sg.Text('Selecione a categoria:')],
            [sg.Listbox(categorias_nomes, size=(40, 10), key='categoria')],
            [sg.Text('')],
            [sg.Button('Próximo', font=('Arial', 10)), sg.Button('Voltar', font=('Arial', 10))],
        ]

        window = sg.Window('Selecionar Categoria', layout_categoria)
        categoria_selecionada = None

        while True:
            event, values = window.read()

            if event in (sg.WIN_CLOSED, 'Voltar'):
                window.close()
                return True

            elif event == 'Próximo':
                if values['categoria']:
                    categoria_nome = values['categoria'][0]
                    categoria_selecionada = self.sistema.categoria_controller.buscar_categoria(categoria_nome)
                    if categoria_selecionada:
                        pode_votar, mensagem = self.sistema.verificar_elegibilidade_voto(categoria_selecionada)
                        if not pode_votar:
                            sg.popup_error(mensagem)
                            continue
                        break
                else:
                    sg.popup_error('Selecione uma categoria!')

        window.close()

        indicados_nomes = []
        for indicado in categoria_selecionada.indicados:
            if isinstance(indicado, str):
                indicados_nomes.append(indicado)
            elif hasattr(indicado, 'nome'):
                indicados_nomes.append(indicado.nome)
            elif hasattr(indicado, 'titulo'):
                indicados_nomes.append(indicado.titulo)
            else:
                indicados_nomes.append(str(indicado))

        layout_voto = [
            [sg.Text(f'CATEGORIA: {categoria_selecionada.nome}', font=('Arial', 14, 'bold'))],
            [sg.Text('')],
            [sg.Text('Selecione seu voto:')],
            [sg.Listbox(indicados_nomes, size=(50, 10), key='indicado')],
            [sg.Text('')],
            [sg.Button('Votar', font=('Arial', 10)), sg.Button('Voltar', font=('Arial', 10))],
        ]

        window = sg.Window('Votar', layout_voto)

        while True:
            event, values = window.read()

            if event in (sg.WIN_CLOSED, 'Voltar'):
                window.close()
                return True

            elif event == 'Votar':
                if values['indicado']:
                    indicado_nome = values['indicado'][0]
                    
                    indicado = None
                    for ind in categoria_selecionada.indicados:
                        if isinstance(ind, str) and ind == indicado_nome:
                            indicado = ind
                            break
                        elif hasattr(ind, 'nome') and ind.nome == indicado_nome:
                            indicado = ind
                            break
                        elif hasattr(ind, 'titulo') and ind.titulo == indicado_nome:
                            indicado = ind
                            break

                    try:
                        sucesso = self.sistema.voto_controller.registrar_voto(
                            self.membro_logado, categoria_selecionada.nome, indicado
                        )

                        if sucesso:
                            sg.popup('Voto registrado com sucesso!', title='Sucesso')
                        else:
                            sg.popup_error('Erro ao registrar voto!')

                        window.close()
                        return True

                    except VotoJaRealizadoException:
                        sg.popup_error('Você já votou nesta categoria!')
                    except PermissaoNegadaException:
                        sg.popup_error('Você não tem permissão para votar!')
                    except DadosInvalidosException as e:
                        sg.popup_error(f'Dados inválidos: {str(e)}')
                    except Exception as e:
                        sg.popup_error(f'Erro ao registrar voto: {str(e)}')
                else:
                    sg.popup_error('Selecione um indicado!')

        window.close()

    def tela_deletar_filme(self):
        filmes = self.sistema.filme_controller.listar_filmes()
        if not filmes:
            sg.popup('Nenhum filme cadastrado!', title='Aviso')
            return True

        filmes_info = [f"{filme.titulo} ({filme.ano}) - {filme.diretor.nome}" for filme in filmes]

        layout = [
            [sg.Text('DELETAR FILME', font=('Arial', 16, 'bold'), text_color='darkred')],
            [sg.Text('')],
            [sg.Text('⚠️ ATENÇÃO: Esta ação não pode ser desfeita!', text_color='red')],
            [sg.Text('')],
            [sg.Text('Selecione o filme a ser deletado:')],
            [sg.Listbox(filmes_info, size=(60, 10), key='filme')],
            [sg.Text('')],
            [sg.Button('Deletar', font=('Arial', 10), button_color=('white', 'darkred')),
             sg.Button('Voltar', font=('Arial', 10))],
        ]

        window = sg.Window('Deletar Filme', layout)

        while True:
            event, values = window.read()

            if event in (sg.WIN_CLOSED, 'Voltar'):
                window.close()
                return True

            elif event == 'Deletar':
                if values['filme']:
                    filme_info = values['filme'][0]
                    titulo = filme_info.split(' (')[0]  
                    resposta = sg.popup_yes_no(
                        f'Tem certeza que deseja deletar o filme "{titulo}"?\n\nEsta ação não pode ser desfeita!',
                        title='Confirmar Exclusão'
                    )

                    if resposta == 'Yes':
                        try:
                            sucesso = self.sistema.filme_controller.excluir_filme(titulo)
                            if sucesso:
                                sg.popup(f'Filme "{titulo}" deletado com sucesso!', title='Sucesso')
                                window.close()
                                return True

                        except ItemNaoEncontradoException as e:
                            sg.popup_error(f'Erro: {e.message}')
                        except PermissaoNegadaException as e:
                            sg.popup_error(f'Erro: {e.message}')
                        except Exception as e:
                            sg.popup_error(f'Erro ao deletar filme: {str(e)}')
                else:
                    sg.popup_error('Selecione um filme!')

        window.close()

    def tela_deletar_ator(self):
        atores = self.sistema.ator_controller.listar_atores()
        if not atores:
            sg.popup('Nenhum ator/atriz cadastrado!', title='Aviso')
            return True

        atores_info = [f"{ator.nome} ({ator.tipo_ator}) - {ator.nacionalidade}" for ator in atores]

        layout = [
            [sg.Text('DELETAR ATOR/ATRIZ', font=('Arial', 16, 'bold'), text_color='darkred')],
            [sg.Text('')],
            [sg.Text('⚠️ ATENÇÃO: Esta ação não pode ser desfeita!', text_color='red')],
            [sg.Text('')],
            [sg.Text('Selecione o ator/atriz a ser deletado:')],
            [sg.Listbox(atores_info, size=(60, 10), key='ator')],
            [sg.Text('')],
            [sg.Button('Deletar', font=('Arial', 10), button_color=('white', 'darkred')),
             sg.Button('Voltar', font=('Arial', 10))],
        ]

        window = sg.Window('Deletar Ator/Atriz', layout)

        while True:
            event, values = window.read()

            if event in (sg.WIN_CLOSED, 'Voltar'):
                window.close()
                return True

            elif event == 'Deletar':
                if values['ator']:
                    ator_info = values['ator'][0]
                    nome = ator_info.split(' (')[0] 
                    resposta = sg.popup_yes_no(
                        f'Tem certeza que deseja deletar o ator/atriz "{nome}"?\n\nEsta ação não pode ser desfeita!',
                        title='Confirmar Exclusão'
                    )

                    if resposta == 'Yes':
                        try:
                            sucesso = self.sistema.ator_controller.excluir_ator(nome)
                            if sucesso:
                                sg.popup(f'Ator/Atriz "{nome}" deletado com sucesso!', title='Sucesso')
                                window.close()
                                return True

                        except ItemNaoEncontradoException as e:
                            sg.popup_error(f'Erro: {e.message}')
                        except PermissaoNegadaException as e:
                            sg.popup_error(f'Erro: {e.message}')
                        except Exception as e:
                            sg.popup_error(f'Erro ao deletar ator: {str(e)}')
                else:
                    sg.popup_error('Selecione um ator/atriz!')

        window.close()

    def tela_editar_filme(self):
        filmes = self.sistema.filme_controller.listar_filmes()
        if not filmes:
            sg.popup('Nenhum filme cadastrado!', title='Aviso')
            return True
        
        filmes_info = [f"{filme.titulo} ({filme.ano}) - {filme.diretor.nome}" for filme in filmes]

        layout_selecao = [
            [sg.Text('EDITAR FILME', font=('Arial', 16, 'bold'))],
            [sg.Text('')],
            [sg.Text('Selecione o filme a ser editado:')],
            [sg.Listbox(filmes_info, size=(60, 10), key='filme')],
            [sg.Text('')],
            [sg.Button('Próximo', font=('Arial', 10)), sg.Button('Voltar', font=('Arial', 10))],
        ]
        
        window = sg.Window('Selecionar Filme', layout_selecao)
        
        while True:
            event, values = window.read()
            
            if event in (sg.WIN_CLOSED, 'Voltar'):
                window.close()
                return True
            
            elif event == 'Próximo':
                if values['filme']:
                    filme_selecionado = values['filme'][0]
                    titulo_atual = filme_selecionado.split(' (')[0]
                    window.close()
                    return self._tela_editar_filme_form(titulo_atual)
                else:
                    sg.popup_error('Selecione um filme!')
        
        window.close()

    def _tela_editar_filme_form(self, titulo_atual):

        filme = self.sistema.filme_controller.buscar_filme(titulo_atual)
        if not filme:
            sg.popup_error('Filme não encontrado!')
            return True
        
        layout = [
            [sg.Text('EDITAR FILME', font=('Arial', 16, 'bold'))],
            [sg.Text(f'Editando: {filme.titulo}', font=('Arial', 12, 'italic'))],
            [sg.Text('')],
            [sg.Text('Novo Título:', size=(12, 1)), 
            sg.Input(default_text=filme.titulo, key='titulo', size=(30, 1))],
            [sg.Text('Novo Ano:', size=(12, 1)), 
            sg.Input(default_text=str(filme.ano), key='ano', size=(30, 1))],
            [sg.Text('Novo Gênero:', size=(12, 1)), 
            sg.Input(default_text=filme.genero, key='genero', size=(30, 1))],
            [sg.Text('Novo Diretor:', size=(12, 1)), 
            sg.Input(default_text=filme.diretor.nome, key='diretor', size=(30, 1))],
            [sg.Text('Nova Descrição:', size=(12, 1)), 
            sg.Multiline(default_text=filme.descricao, key='descricao', size=(30, 4))],
            [sg.Text('')],
            [sg.Button('Salvar Alterações', font=('Arial', 10)), 
            sg.Button('Cancelar', font=('Arial', 10))],
        ]
        
        window = sg.Window('Editar Filme', layout)
        
        while True:
            event, values = window.read()
            
            if event in (sg.WIN_CLOSED, 'Cancelar'):
                window.close()
                return True
            
            elif event == 'Salvar Alterações':
                try:

                    novo_titulo = values['titulo'].strip() if values['titulo'].strip() != filme.titulo else None
                    novo_ano = None
                    if values['ano'].strip() and values['ano'].strip() != str(filme.ano):
                        novo_ano = int(values['ano'])
                    
                    novo_genero = values['genero'].strip() if values['genero'].strip() != filme.genero else None
                    novo_diretor = values['diretor'].strip() if values['diretor'].strip() != filme.diretor.nome else None
                    nova_descricao = values['descricao'].strip() if values['descricao'].strip() != filme.descricao else None

                    if not any([novo_titulo, novo_ano, novo_genero, novo_diretor, nova_descricao]):
                        sg.popup('Nenhuma alteração foi feita!', title='Aviso')
                        continue
                    
                    filme_editado = self.sistema.filme_controller.editar_filme(
                        titulo_atual, novo_titulo, novo_ano, novo_genero, 
                        novo_diretor, nova_descricao
                    )
                    
                    alteracoes = []
                    if novo_titulo: alteracoes.append(f"Título: {novo_titulo}")
                    if novo_ano: alteracoes.append(f"Ano: {novo_ano}")
                    if novo_genero: alteracoes.append(f"Gênero: {novo_genero}")
                    if novo_diretor: alteracoes.append(f"Diretor: {novo_diretor}")
                    if nova_descricao: alteracoes.append("Descrição atualizada")
                    
                    mensagem_sucesso = f'Filme editado com sucesso!\n\nAlterações realizadas:\n' + '\n'.join(alteracoes)
                    sg.popup(mensagem_sucesso, title='Sucesso')
                    window.close()
                    return True
                    
                except ValueError:
                    sg.popup_error('Ano deve ser um número válido!')
                except DadosInvalidosException as e:
                    sg.popup_error(f'Dados inválidos: {e.message}')
                except ItemNaoEncontradoException as e:
                    sg.popup_error(f'Erro: {e.message}')
                except PermissaoNegadaException as e:
                    sg.popup_error(f'Erro: {e.message}')
                except Exception as e:
                    sg.popup_error(f'Erro ao editar filme: {str(e)}')
            
        window.close()


    def tela_deletar_indicacao(self):
        indicacoes = self.sistema.indicacao_controller.listar_indicacoes()
        if not indicacoes:
            sg.popup('Nenhuma indicação cadastrada!', title='Aviso')
            return True

        indicacoes_info = []
        indicacoes_dados = []  

        for indicacao in indicacoes:
            categoria_nome = indicacao.categoria.nome

            if isinstance(indicacao.indicado, str):
                indicado_nome = indicacao.indicado
            elif hasattr(indicacao.indicado, 'nome'):
                indicado_nome = indicacao.indicado.nome
            elif hasattr(indicacao.indicado, 'titulo'):
                indicado_nome = indicacao.indicado.titulo
            else:
                indicado_nome = str(indicacao.indicado)

            display_text = f"[{categoria_nome}] {indicado_nome}"
            indicacoes_info.append(display_text)
            indicacoes_dados.append((categoria_nome, indicacao.indicado))

        layout = [
            [sg.Text('DELETAR INDICAÇÃO', font=('Arial', 16, 'bold'), text_color='darkred')],
            [sg.Text('')],
            [sg.Text('⚠️ ATENÇÃO: Esta ação não pode ser desfeita!', text_color='red')],
            [sg.Text('⚠️ Votos relacionados a esta indicação podem ser afetados!', text_color='orange')],
            [sg.Text('')],
            [sg.Text('Selecione a indicação a ser deletada:')],
            [sg.Listbox(indicacoes_info, size=(70, 12), key='indicacao')],
            [sg.Text('')],
            [sg.Button('Deletar', font=('Arial', 10), button_color=('white', 'darkred')),
             sg.Button('Voltar', font=('Arial', 10))],
        ]

        window = sg.Window('Deletar Indicação', layout)

        while True:
            event, values = window.read()

            if event in (sg.WIN_CLOSED, 'Voltar'):
                window.close()
                return True

            elif event == 'Deletar':
                if values['indicacao']:
                    indice_selecionado = indicacoes_info.index(values['indicacao'][0])
                    categoria_nome, indicado = indicacoes_dados[indice_selecionado]

                    if isinstance(indicado, str):
                        nome_indicado = indicado
                    elif hasattr(indicado, 'nome'):
                        nome_indicado = indicado.nome
                    elif hasattr(indicado, 'titulo'):
                        nome_indicado = indicado.titulo
                    else:
                        nome_indicado = str(indicado)

                    resposta = sg.popup_yes_no(
                        f'Tem certeza que deseja deletar esta indicação?\n\n'
                        f'Categoria: {categoria_nome}\n'
                        f'Indicado: {nome_indicado}\n\n'
                        f'AVISO: Votos relacionados podem ser afetados!\n\n'
                        f'Esta ação não pode ser desfeita!',
                        title='Confirmar Exclusão'
                    )

                    if resposta == 'Yes':
                        try:
                            sucesso = self.sistema.indicacao_controller.deletar_indicacao(categoria_nome, indicado)
                            if sucesso:
                                sg.popup(
                                    f'Indicação deletada com sucesso!\n\n'
                                    f'Categoria: {categoria_nome}\n'
                                    f'Indicado: {nome_indicado}',
                                    title='Sucesso'
                                )
                                window.close()
                                return True
                            else:
                                sg.popup_error('Erro ao deletar indicação! Verifique se a indicação ainda existe.')

                        except ItemNaoEncontradoException as e:
                            sg.popup_error(f'Erro: {e.message}')
                        except PermissaoNegadaException as e:
                            sg.popup_error(f'Erro: {e.message}')
                        except Exception as e:
                            sg.popup_error(f'Erro ao deletar indicação: {str(e)}')
                else:
                    sg.popup_error('Selecione uma indicação!')

        window.close()

    def mostrar_relatorio(self):
        try:
            relatorio = self.sistema.gerar_relatorio_completo()
        except ArquivoException as e:
            relatorio = f"Erro ao acessar arquivo: {str(e)}"
        except Exception as e:
            relatorio = f"Erro ao gerar relatório: {str(e)}"

        layout = [
            [sg.Text('RELATÓRIO DO OSCAR', font=('Arial', 16, 'bold'))],
            [sg.Multiline(relatorio, size=(80, 20), disabled=True)],
            [sg.Button('Fechar', font=('Arial', 10))],
        ]

        window = sg.Window('Relatório', layout)

        while True:
            event, values = window.read()

            if event in (sg.WIN_CLOSED, 'Fechar'):
                break

        window.close()

    def executar(self):
        self.tela_principal()

if __name__ == "__main__":
    app = TelaPrincipal()
    app.executar()