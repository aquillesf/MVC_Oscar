# main.py
from controllers.sistema_oscar_controller import SistemaOscarController
from views.sistema_oscar_view import SistemaOscarView

class OscarApplication:
    def __init__(self):
        self.__sistema_controller = SistemaOscarController()
        self.__sistema_view = SistemaOscarView()
        self.__membro_logado = None
    
    @property
    def sistema_controller(self):
        return self.__sistema_controller
    
    @property
    def sistema_view(self):
        return self.__sistema_view
    
    @property
    def membro_logado(self):
        return self.__membro_logado
    
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
        dados = self.__sistema_view.membro_view.solicitar_dados_membro()
        if dados:
            nome, tipo = dados
            membro = self.__sistema_controller.membro_controller.criar_membro(nome, tipo)
            if membro:
                self.__sistema_view.mostrar_mensagem_sucesso("Cadastro realizado com sucesso!")
            else:
                self.__sistema_view.mostrar_mensagem_erro("Erro ao cadastrar membro.")
    
    def __fazer_login(self):
        nome = self.__sistema_view.membro_view.solicitar_login()
        membro = self.__sistema_controller.membro_controller.login(nome)
        
        if membro:
            self.__membro_logado = membro
            print(f"Bem-vindo, {membro.nome} ({membro.tipo})!")
            self.__menu_logado()
        else:
            self.__sistema_view.mostrar_mensagem_erro("Membro não encontrado.")
    
    def __menu_logado(self):
        while self.__membro_logado:
            opcao = self.__sistema_view.mostrar_menu_logado(self.__membro_logado)
            
            if opcao == "1" and self.__membro_logado.pode_registrar():
                self.__adicionar_filme()
            elif opcao == "2" and self.__membro_logado.pode_registrar():
                self.__adicionar_ator()
            elif opcao == "3" and self.__membro_logado.pode_registrar():
                self.__adicionar_indicacao()
            elif opcao == "4" and self.__membro_logado.pode_votar():
                self.__votar()
            elif opcao == "5":
                self.__gerar_relatorio()
            elif opcao == "6":
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
        categoria = self.__sistema_view.categoria_view.selecionar_categoria(
            self.__sistema_controller.categoria_controller.listar_categorias()
        )
        
        if categoria and categoria.indicados:
            indicado = self.__sistema_view.voto_view.solicitar_voto(categoria)
            if indicado:
                sucesso = self.__sistema_controller.voto_controller.registrar_voto(
                    self.__membro_logado, categoria.nome, indicado
                )
                if sucesso:
                    self.__sistema_view.mostrar_mensagem_sucesso("Voto registrado com sucesso!")
                else:
                    self.__sistema_view.mostrar_mensagem_erro("Erro ao registrar voto. Você já pode ter votado nesta categoria.")
        elif categoria:
            self.__sistema_view.mostrar_mensagem_erro("Esta categoria não possui indicados.")
    
    def __gerar_relatorio(self):
        relatorio = self.__gerar_relatorio_completo()
        self.__sistema_view.mostrar_relatorio(relatorio)
    
    def __gerar_relatorio_completo(self):
        relatorio = "=== RELATÓRIO DO SISTEMA OSCAR ===\n\n"
        total_membros = len(self.__sistema_controller.membro_controller.listar_membros())
        total_filmes = len(self.__sistema_controller.filme_controller.listar_filmes())
        total_atores = len(self.__sistema_controller.ator_controller.listar_atores())
        total_diretores = len(self.__sistema_controller.diretor_controller.listar_diretores())
        total_votos = len(self.__sistema_controller.voto_controller.listar_votos())
        
        relatorio += f"📊 ESTATÍSTICAS GERAIS\n"
        relatorio += f"Membros cadastrados: {total_membros}\n"
        relatorio += f"Filmes cadastrados: {total_filmes}\n"
        relatorio += f"Atores cadastrados: {total_atores}\n"
        relatorio += f"Diretores cadastrados: {total_diretores}\n"
        relatorio += f"Total de votos: {total_votos}\n\n"
        relatorio += "🏆 RESULTADOS POR CATEGORIA\n"
        categorias = self.__sistema_controller.categoria_controller.listar_categorias()
        
        for categoria in categorias:
            relatorio += f"\n--- {categoria.nome} ---\n"
            if categoria.indicados:
                contagem = self.__sistema_controller.voto_controller.contar_votos_categoria(categoria)
                if contagem:
                    resultados = sorted(contagem.items(), key=lambda x: x[1], reverse=True)
                    for i, (indicado, votos) in enumerate(resultados, 1):
                        emoji = ["🥇", "🥈", "🥉", "📍"][i - 1] if i <= 4 else "📍"
                        if isinstance(indicado, str):
                            nome = indicado
                        elif hasattr(indicado, "nome"):
                            nome = indicado.nome
                        elif hasattr(indicado, "titulo"):
                            nome = indicado.titulo
                        else:
                            nome = str(indicado)
                        relatorio += f"{emoji} {nome}: {votos} voto(s)\n"
                else:
                    relatorio += "Nenhum voto registrado ainda.\n"
                
                relatorio += f"Indicados: {len(categoria.indicados)}\n"
                for indicado in categoria.indicados:
                    if isinstance(indicado, str):
                        nome = indicado
                    elif hasattr(indicado, "nome"):
                        nome = indicado.nome
                    elif hasattr(indicado, "titulo"):
                        nome = indicado.titulo
                    else:
                        nome = str(indicado)

                    relatorio += f" {nome}\n"
            else:
                relatorio += "Nenhum indicado cadastrado.\n"
        
        return relatorio
    
    def __logout(self):
        """Realiza logout do usuário"""
        print(f"Até logo, {self.__membro_logado.nome}!")
        self.__membro_logado = None


def main():
    """Função principal da aplicação"""
    print(" ")
    print("=== SISTEMA DE VOTAÇÃO DO OSCAR ===")
    print("Bem-vindo ao sistema de gerenciamento do Oscar!\n")
    
    app = OscarApplication()
    app.executar()

if __name__ == "__main__":
    main()