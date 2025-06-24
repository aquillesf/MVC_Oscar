import PySimpleGUI as sg
from controllers.sistema_oscar_controller import SistemaOscarController

class OscarGUI:
    def __init__(self):
        self.sistema = SistemaOscarController()
        self.membro_logado = None
        sg.theme('DarkBlue3')
        
    def tela_principal(self):
        """Tela inicial do sistema"""
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
                self.tela_cadastro()
                break
            elif event == 'Login':
                window.close()
                self.tela_login()
                break
        
        window.close()
    
    def tela_cadastro(self):
        """Tela de cadastro de membro"""
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
                self.tela_principal()
                break
            elif event == 'Cadastrar':
                if values['nome'] and values['senha'] and values['tipo']:
                    try:
                        sucesso, mensagem = self.sistema.cadastrar_membro(
                            values['nome'], values['tipo'], values['senha']
                        )
                        if sucesso:
                            sg.popup(mensagem, title='Sucesso')
                            window.close()
                            self.tela_principal()
                            break
                        else:
                            sg.popup_error(mensagem)
                    except Exception as e:
                        sg.popup_error(f'Erro ao cadastrar membro: {str(e)}')
                else:
                    sg.popup_error('Preencha todos os campos!')
        
        window.close()
    
    def tela_login(self):
        """Tela de login"""
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
                self.tela_principal()
                break
            elif event == 'Entrar':
                if values['nome'] and values['senha']:
                    try:
                        sucesso, mensagem = self.sistema.fazer_login(values['nome'], values['senha'])
                        if sucesso:
                            self.membro_logado = self.sistema.membro_logado
                            sg.popup(mensagem, title='Login realizado')
                            window.close()
                            self.tela_menu_principal()
                            break
                        else:
                            sg.popup_error(mensagem)
                    except Exception as e:
                        sg.popup_error(f'Erro no login: {str(e)}')
                else:
                    sg.popup_error('Digite nome e senha!')
        
        window.close()
    
    def tela_menu_principal(self):
        """Menu principal após login - VERSÃO ATUALIZADA COM OPÇÕES DE DELETAR"""
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
        
        while True:
            event, values = window.read()
            
            if event in (sg.WIN_CLOSED, 'Logout'):
                self.sistema.fazer_logout()
                self.membro_logado = None
                window.close()
                self.tela_principal()
                break
            elif event == 'Adicionar Filme':
                window.close()
                self.tela_adicionar_filme()
                break
            elif event == 'Alterar Senha':
                window.close()
                self.tela_alterar_senha()
                break
            elif event == 'Adicionar Ator/Atriz':
                window.close()
                self.tela_adicionar_ator()
                break
            elif event == 'Adicionar Indicação':
                window.close()
                self.tela_adicionar_indicacao()
                break
            elif event == 'Votar em Categoria':
                window.close()
                self.tela_votar()
                break
            elif event == 'Deletar Filme':
                window.close()
                self.tela_deletar_filme()
                break
            elif event == 'Deletar Ator/Atriz':
                window.close()
                self.tela_deletar_ator()
                break
            elif event == 'Deletar Indicação':
                window.close()
                self.tela_deletar_indicacao()
                break
            elif event == 'Gerar Relatório':
                self.mostrar_relatorio()
        
        window.close()

    def tela_deletar_filme(self):
        """Tela para deletar filme"""
        filmes = self.sistema.filme_controller.listar_filmes()
        
        if not filmes:
            sg.popup('Nenhum filme cadastrado!', title='Aviso')
            self.tela_menu_principal()
            return
        
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
                self.tela_menu_principal()
                break
            elif event == 'Deletar':
                if values['filme']:
                    filme_info = values['filme'][0]
                    titulo = filme_info.split(' (')[0]  # Extrai o título
                    
                    # Confirmação
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
                                self.tela_menu_principal()
                                break
                        except Exception as e:
                            sg.popup_error(f'Erro ao deletar filme: {str(e)}')
                else:
                    sg.popup_error('Selecione um filme!')
        
        window.close()
    
    def tela_deletar_ator(self):
        """Tela para deletar ator/atriz"""
        atores = self.sistema.ator_controller.listar_atores()
        
        if not atores:
            sg.popup('Nenhum ator/atriz cadastrado!', title='Aviso')
            self.tela_menu_principal()
            return
        
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
                self.tela_menu_principal()
                break
            elif event == 'Deletar':
                if values['ator']:
                    ator_info = values['ator'][0]
                    nome = ator_info.split(' (')[0]  # Extrai o nome
                    
                    # Confirmação
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
                                self.tela_menu_principal()
                                break
                        except Exception as e:
                            sg.popup_error(f'Erro ao deletar ator: {str(e)}')
                else:
                    sg.popup_error('Selecione um ator/atriz!')
        
        window.close()

    def tela_deletar_indicacao(self):
        """Tela para deletar indicação"""
        indicacoes = self.sistema.indicacao_controller.listar_indicacoes()
        
        if not indicacoes:
            sg.popup('Nenhuma indicação cadastrada!', title='Aviso')
            self.tela_menu_principal()
            return
        
        # Criar lista de indicações organizadas por categoria
        indicacoes_info = []
        indicacoes_dados = []  # Para guardar os dados originais
        
        for indicacao in indicacoes:
            categoria_nome = indicacao.categoria.nome
            
            # Extrair nome do indicado baseado no tipo
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
                self.tela_menu_principal()
                break
            elif event == 'Deletar':
                if values['indicacao']:
                    # Encontrar qual indicação foi selecionada
                    indice_selecionado = indicacoes_info.index(values['indicacao'][0])
                    categoria_nome, indicado = indicacoes_dados[indice_selecionado]
                    
                    # Obter nome para exibição
                    if isinstance(indicado, str):
                        nome_indicado = indicado
                    elif hasattr(indicado, 'nome'):
                        nome_indicado = indicado.nome
                    elif hasattr(indicado, 'titulo'):
                        nome_indicado = indicado.titulo
                    else:
                        nome_indicado = str(indicado)
                    
                    # Confirmação
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
                                self.tela_menu_principal()
                                break
                            else:
                                sg.popup_error('Erro ao deletar indicação! Verifique se a indicação ainda existe.')
                        except Exception as e:
                            sg.popup_error(f'Erro ao deletar indicação: {str(e)}')
                else:
                    sg.popup_error('Selecione uma indicação!')
        
        window.close()

    def tela_alterar_senha(self):
        """Tela para alterar senha do usuário logado"""
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
                self.tela_menu_principal()
                break
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
                            self.tela_menu_principal()
                            break
                        else:
                            sg.popup_error(mensagem)
                    except Exception as e:
                        sg.popup_error(f'Erro ao alterar senha: {str(e)}')
                else:
                    sg.popup_error('Preencha todos os campos!')
        window.close()
    
    def tela_adicionar_filme(self):
        """Tela para adicionar filme"""
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
                self.tela_menu_principal()
                break
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
                        self.tela_menu_principal()
                        break
                    except ValueError:
                        sg.popup_error('Ano deve ser um número válido!')
                    except Exception as e:
                        sg.popup_error(f'Erro ao adicionar filme: {str(e)}')
                else:
                    sg.popup_error('Preencha todos os campos obrigatórios!')
        
        window.close()
    
    def tela_adicionar_ator(self):
        """Tela para adicionar ator/atriz"""
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
                self.tela_menu_principal()
                break
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
                        self.tela_menu_principal()
                        break
                    except ValueError:
                        sg.popup_error('Idade deve ser um número!')
                    except Exception as e:
                        sg.popup_error(f'Erro ao adicionar ator: {str(e)}')
                else:
                    sg.popup_error('Preencha todos os campos!')
        
        window.close()
    
    def tela_adicionar_indicacao(self):
        """Tela para adicionar indicação"""
        categorias = self.sistema.categoria_controller.listar_categorias()
        
        if not categorias:
            sg.popup_error('Nenhuma categoria disponível!')
            self.tela_menu_principal()
            return
        
        # Selecionar categoria
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
                self.tela_menu_principal()
                return
            elif event == 'Próximo':
                if values['categoria']:
                    categoria_nome = values['categoria'][0]
                    categoria_selecionada = self.sistema.categoria_controller.buscar_categoria(categoria_nome)
                    if categoria_selecionada:
                        break
                else:
                    sg.popup_error('Selecione uma categoria!')
        
        window.close()
        
        # Selecionar indicado baseado na categoria
        indicados = []
        if "Filme" in categoria_selecionada.nome:
            filmes = self.sistema.filme_controller.listar_filmes()
            indicados = [f"{filme.titulo} ({filme.ano})" for filme in filmes]
        elif "Diretor" in categoria_selecionada.nome:
            diretores = self.sistema.diretor_controller.listar_diretores()
            indicados = [diretor.nome for diretor in diretores]
        else:  # Categorias de ator
            atores = self.sistema.ator_controller.listar_atores()
            indicados = [f"{ator.nome} ({ator.tipo_ator})" for ator in atores]
        
        if not indicados:
            sg.popup_error('Não há itens disponíveis para esta categoria!')
            self.tela_menu_principal()
            return
        
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
                self.tela_menu_principal()
                break
            elif event == 'Adicionar':
                if values['indicado']:
                    indicado_str = values['indicado'][0]
                    
                    # Extrair nome/título baseado no tipo
                    if "Filme" in categoria_selecionada.nome:
                        # Buscar o filme original
                        titulo = indicado_str.split(' (')[0]
                        filme = self.sistema.filme_controller.buscar_filme(titulo)
                        indicado = filme
                    elif "Diretor" in categoria_selecionada.nome:
                        diretor = self.sistema.diretor_controller.buscar_diretor(indicado_str)
                        indicado = diretor
                    else:  # Ator
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
                        self.tela_menu_principal()
                        break
                    except Exception as e:
                        sg.popup_error(f'Erro ao adicionar indicação: {str(e)}')
                else:
                    sg.popup_error('Selecione um indicado!')
        
        window.close()
    
    def tela_votar(self):
        """Tela para votar em categoria"""
        categorias = self.sistema.categoria_controller.listar_categorias()
        categorias_com_indicados = [cat for cat in categorias if cat.indicados]
        
        if not categorias_com_indicados:
            sg.popup('Nenhuma categoria com indicados disponível para votação!', title='Aviso')
            self.tela_menu_principal()
            return
        
        # Selecionar categoria
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
                self.tela_menu_principal()
                return
            elif event == 'Próximo':
                if values['categoria']:
                    categoria_nome = values['categoria'][0]
                    categoria_selecionada = self.sistema.categoria_controller.buscar_categoria(categoria_nome)
                    if categoria_selecionada:
                        # Verificar se pode votar
                        pode_votar, mensagem = self.sistema.verificar_elegibilidade_voto(categoria_selecionada)
                        if not pode_votar:
                            sg.popup_error(mensagem)
                            continue
                        break
                else:
                    sg.popup_error('Selecione uma categoria!')
        
        window.close()
        
        # Mostrar indicados para votação
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
                self.tela_menu_principal()
                break
            elif event == 'Votar':
                if values['indicado']:
                    indicado_nome = values['indicado'][0]
                    
                    # Encontrar o indicado original
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
                        self.tela_menu_principal()
                        break
                    except Exception as e:
                        sg.popup_error(f'Erro ao registrar voto: {str(e)}')
                else:
                    sg.popup_error('Selecione um indicado!')
        
        window.close()
    
    def mostrar_relatorio(self):
        """Mostrar relatório em popup"""
        try:
            relatorio = self.sistema.gerar_relatorio_completo()
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
        """Método principal para executar a aplicação"""
        self.tela_principal()

if __name__ == '__main__':
    app = OscarGUI()
    app.executar()