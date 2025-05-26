from controllers.sistema_oscar_controller import SistemaOscarController
from views.sistema_oscar_view import SistemaOscarView

class OscarApplication:
    def __init__(self):
        self.__sistema_controller = SistemaOscarController()
        self.__sistema_view = SistemaOscarView()
    
    @property
    def sistema_controller(self):
        return self.__sistema_controller
    
    @property
    def sistema_view(self):
        return self.__sistema_view
    
    def executar(self):
        while True:
            opcao = self.__sistema_view.mostrar_menu_principal()
            
            if opcao == "1":
                self.__cadastrar_membro()
            elif opcao == "2":
                self.__fazer_login()
            elif opcao == "3":
                print("Saindo do sistema...")
                break
            else:
                self.__sistema_view.mostrar_mensagem_erro("Opção inválida. Tente novamente.")
    
    def __cadastrar_membro(self):
        dados = self.__sistema_view.solicitar_dados_cadastro()
        if dados[0]: 
            nome, tipo, senha = dados
            sucesso, mensagem = self.__sistema_controller.cadastrar_membro(nome, tipo, senha)
            
            if sucesso:
                self.__sistema_view.mostrar_mensagem_sucesso(mensagem)
            else:
                self.__sistema_view.mostrar_mensagem_erro(mensagem)
    
    def __fazer_login(self):
        nome, senha = self.__sistema_view.solicitar_dados_login()
        sucesso, mensagem = self.__sistema_controller.fazer_login(nome, senha)
        
        if sucesso:
            self.__sistema_view.mostrar_mensagem_sucesso(mensagem)
            self.__menu_logado()
        else:
            self.__sistema_view.mostrar_mensagem_erro(mensagem)
    
    def __menu_logado(self):
        while self.__sistema_controller.verificar_autenticacao():
            permissoes = self.__sistema_controller.obter_permissoes_usuario()
            opcao = self.__sistema_view.mostrar_menu_logado(permissoes)
            
            if not opcao:
                self.__sistema_view.mostrar_mensagem_erro("Opção inválida.")
                continue
            
            if opcao == "1" and permissoes['pode_registrar']:
                self.__adicionar_filme()
            elif opcao == "2" and permissoes['pode_registrar']:
                self.__adicionar_ator()
            elif opcao == "3" and permissoes['pode_registrar']:
                self.__adicionar_indicacao()
            elif opcao == "4" and permissoes['pode_votar']:
                self.__votar()
            elif opcao == "5":
                self.__gerar_relatorio()
            elif opcao == "6":
                self.__alterar_senha()
            elif opcao == "7":
                self.__logout()
            else:
                self.__sistema_view.mostrar_mensagem_erro("Opção inválida ou sem permissão.")
    
    def __adicionar_filme(self):
        dados = self.__sistema_view.filme_view.solicitar_dados_filme()
        if dados:
            titulo, ano, genero, diretor, descricao = dados
            try:
                ano = int(ano)
                filme = self.__sistema_controller.filme_controller.criar_filme(
                    titulo, ano, genero, diretor, descricao
                )
                if filme:
                    self.__sistema_view.mostrar_mensagem_sucesso("Filme adicionado com sucesso!")
                else:
                    self.__sistema_view.mostrar_mensagem_erro("Erro ao adicionar filme.")
            except ValueError:
                self.__sistema_view.mostrar_mensagem_erro("Ano deve ser um número válido.")
    
    def __adicionar_ator(self):
        dados = self.__sistema_view.ator_view.solicitar_dados_ator()
        if dados:
            nome, idade, filmes, tipo, nacionalidade = dados
            ator = self.__sistema_controller.ator_controller.criar_ator(
                nome, idade, filmes, tipo, nacionalidade
            )
            if ator:
                self.__sistema_view.mostrar_mensagem_sucesso("Ator/Atriz adicionado(a) com sucesso!")
            else:
                self.__sistema_view.mostrar_mensagem_erro("Erro ao adicionar ator/atriz.")
    
    def __adicionar_indicacao(self):
        categoria = self.__sistema_view.categoria_view.selecionar_categoria(
            self.__sistema_controller.categoria_controller.listar_categorias()
        )
        
        if categoria:
            if categoria.nome in ["Melhor Filme"]:
                filmes = self.__sistema_controller.filme_controller.listar_filmes()
                if filmes:
                    self.__sistema_view.filme_view.listar_filmes(filmes)
                    try:
                        opcao = int(input("Escolha o número do filme: ")) - 1
                        filme = filmes[opcao]
                        indicacao = self.__sistema_controller.indicacao_controller.criar_indicacao(
                            categoria.nome, filme
                        )
                        if indicacao:
                            self.__sistema_view.mostrar_mensagem_sucesso("Indicação criada com sucesso!")
                        else:
                            self.__sistema_view.mostrar_mensagem_erro("Erro ao criar indicação.")
                    except (ValueError, IndexError):
                        self.__sistema_view.mostrar_mensagem_erro("Opção inválida.")
                else:
                    self.__sistema_view.mostrar_mensagem_erro("Nenhum filme cadastrado.")
            
            elif categoria.nome in ["Melhor Ator", "Melhor Atriz", "Melhor Ator Coadjuvante", "Melhor Atriz Coadjuvante"]:
                atores = self.__sistema_controller.ator_controller.listar_atores()
                if atores:
                    self.__sistema_view.ator_view.listar_atores(atores)
                    try:
                        opcao = int(input("Escolha o número do ator/atriz: ")) - 1
                        ator = atores[opcao]
                        indicacao = self.__sistema_controller.indicacao_controller.criar_indicacao(
                            categoria.nome, ator
                        )
                        if indicacao:
                            self.__sistema_view.mostrar_mensagem_sucesso("Indicação criada com sucesso!")
                        else:
                            self.__sistema_view.mostrar_mensagem_erro("Erro ao criar indicação.")
                    except (ValueError, IndexError):
                        self.__sistema_view.mostrar_mensagem_erro("Opção inválida.")
                else:
                    self.__sistema_view.mostrar_mensagem_erro("Nenhum ator/atriz cadastrado.")
            
            elif categoria.nome == "Melhor Diretor":
                diretores = self.__sistema_controller.diretor_controller.listar_diretores()
                if diretores:
                    self.__sistema_view.diretor_view.listar_diretores(diretores)
                    try:
                        opcao = int(input("Escolha o número do diretor: ")) - 1
                        diretor = diretores[opcao]
                        indicacao = self.__sistema_controller.indicacao_controller.criar_indicacao(
                            categoria.nome, diretor
                        )
                        if indicacao:
                            self.__sistema_view.mostrar_mensagem_sucesso("Indicação criada com sucesso!")
                        else:
                            self.__sistema_view.mostrar_mensagem_erro("Erro ao criar indicação.")
                    except (ValueError, IndexError):
                        self.__sistema_view.mostrar_mensagem_erro("Opção inválida.")
                else:
                    self.__sistema_view.mostrar_mensagem_erro("Nenhum diretor cadastrado.")
    
    def __votar(self):
        categorias = self.__sistema_controller.categoria_controller.listar_categorias()
        categoria = self.__sistema_view.categoria_view.selecionar_categoria(categorias)

        if not categoria:
            self.__sistema_view.mostrar_mensagem_erro("Categoria inválida ou não selecionada.")
            return

        pode_votar, mensagem = self.__sistema_controller.verificar_elegibilidade_voto(categoria)
        if not pode_votar:
            self.__sistema_view.mostrar_mensagem_erro(mensagem)
            return

        if not categoria.indicados:
            self.__sistema_view.mostrar_mensagem_erro("Esta categoria não possui indicados.")
            return
        
        if not hasattr(self.__sistema_view, 'voto_view'):
            self.__sistema_view.mostrar_mensagem_erro("Erro interno: voto_view não está disponível.")
            return

        indicado = self.__sistema_view.voto_view.solicitar_voto(categoria)
        if not indicado:
            self.__sistema_view.mostrar_mensagem_erro("Indicado inválido ou não selecionado.")
            return

        sucesso = self.__sistema_controller.voto_controller.registrar_voto(
            self.__sistema_controller.membro_logado, categoria.nome, indicado
        )

        if sucesso:
            self.__sistema_view.mostrar_mensagem_sucesso("Voto registrado com sucesso!")
        else:
            self.__sistema_view.mostrar_mensagem_erro("Erro ao registrar voto.")
    
    def __gerar_relatorio(self):
        relatorio_completo = self.__sistema_controller.gerar_relatorio_completo()
        
        categorias = self.__sistema_controller.categoria_controller.listar_categorias()
        relatorios_categoria = ""
        if categorias:
            for categoria in categorias:
                rel = self.__sistema_controller.gerar_relatorio_categoria(categoria.nome)
                relatorios_categoria += f"\n--- Relatório da Categoria: {categoria.nome} ---\n"
                relatorios_categoria += rel + "\n"
        else:
            relatorios_categoria = "\nNenhuma categoria cadastrada.\n"
        
        vencedores = self.__sistema_controller.obter_vencedores()
        relatorio_vencedores = "\n=== VENCEDORES ATUAIS ===\n"
        if isinstance(vencedores, dict) and vencedores:
            for categoria, dados in vencedores.items():
                relatorio_vencedores += f"🏆 {categoria}: {dados['indicado']} ({dados['votos']} votos)\n"
        else:
            relatorio_vencedores += "Nenhum resultado disponível ainda.\n"
        
        relatorio_final = (
            "=== RELATÓRIO COMPLETO ===\n"
            + relatorio_completo
            + "\n\n=== RELATÓRIOS POR CATEGORIA ==="
            + relatorios_categoria
            + "\n"
            + relatorio_vencedores
        )
        
        self.__sistema_view.mostrar_relatorio(relatorio_final)

    
    def __alterar_senha(self):
        dados = self.__sistema_view.solicitar_alteracao_senha()
        if dados[0]:  
            senha_atual, nova_senha = dados
            sucesso, mensagem = self.__sistema_controller.alterar_senha(senha_atual, nova_senha)
            
            if sucesso:
                self.__sistema_view.mostrar_mensagem_sucesso(mensagem)
            else:
                self.__sistema_view.mostrar_mensagem_erro(mensagem)
    
    def __logout(self):
        sucesso, mensagem = self.__sistema_controller.fazer_logout()
        self.__sistema_view.mostrar_mensagem_sucesso(mensagem)


def main():
    print(" ")
    print("=== SISTEMA DE VOTAÇÃO DO OSCAR ===")
    print("Bem-vindo ao sistema de gerenciamento do Oscar!")
    
    app = OscarApplication()
    app.executar()

if __name__ == "__main__":
    main()