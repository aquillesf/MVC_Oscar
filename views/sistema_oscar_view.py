from views.pessoa_view import PessoaView
from views.artista_view import ArtistaView
from views.ator_view import AtorView
from views.diretor_view import DiretorView
from views.filme_view import FilmeView
from views.categoria_view import CategoriaView
from views.membro_view import MembroView
from views.voto_view import VotoView
from views.indicacao_view import IndicacaoView

class SistemaOscarView:
    def __init__(self):
        self.__pessoa_view = PessoaView()
        self.__artista_view = ArtistaView()
        self.__ator_view = AtorView()
        self.__diretor_view = DiretorView()
        self.__filme_view = FilmeView()
        self.__categoria_view = CategoriaView()
        self.__membro_view = MembroView()
        self.__voto_view = VotoView()
        self.__indicacao_view = IndicacaoView()
    
    @property
    def pessoa_view(self):
        return self.__pessoa_view
    
    @property
    def artista_view(self):
        return self.__artista_view
    
    @property
    def ator_view(self):
        return self.__ator_view
    
    @property
    def diretor_view(self):
        return self.__diretor_view
    
    @property
    def filme_view(self):
        return self.__filme_view
    
    @property
    def categoria_view(self):
        return self.__categoria_view
    
    @property
    def membro_view(self):
        return self.__membro_view
    
    @property
    def voto_view(self):
        return self.__voto_view

    @property
    def indicacao_view(self):
        return self.__indicacao_view
    
    def mostrar_menu_principal(self):
        print("\n=== SISTEMA DO OSCAR ===")
        print("1. Cadastrar-se")
        print("2. Login")
        print("3. Sair")
        return input("Escolha uma opção: ")
    
    def solicitar_dados_cadastro(self):
        print("\n=== CADASTRO DE MEMBRO ===")
        nome = input("Nome: ").strip()
        
        print("\nTipos de membro:")
        print("1. VOTADOR (pode votar)")
        print("2. REGISTRADOR (pode registrar filmes/indicações)")
        
        opcao_tipo = input("Escolha o tipo (1 ou 2): ")
        tipo = 'VOTADOR' if opcao_tipo == '1' else 'REGISTRADOR' if opcao_tipo == '2' else None
        
        if not tipo:
            return None, None, None
        
        senha = input("Senha: ")
        confirmar_senha = input("Confirme a senha: ")
        
        if senha != confirmar_senha:
            print("Senhas não coincidem!")
            return None, None, None
        
        return nome, tipo, senha
    
    def solicitar_dados_login(self):
        print("\n=== LOGIN ===")
        nome = input("Nome: ").strip()
        senha = input("Senha: ")
        return nome, senha
    
    def mostrar_menu_logado(self, permissoes):
        print(f"\n=== MENU PRINCIPAL - {permissoes['nome']} ({permissoes['tipo']}) ===")
        
        opcoes = []
        
        if permissoes['pode_registrar']:
            print("1. Adicionar Filme")
            print("2. Adicionar Ator/Atriz")
            print("3. Adicionar Indicação")
            opcoes.extend(['1', '2', '3'])
        
        if permissoes['pode_votar']:
            print("4. Votar em uma categoria")
            opcoes.append('4')
        
        print("5. Gerar relatório")
        print("6. Alterar senha")
        print("7. Logout")
        opcoes.extend(['5', '6', '7'])
        
        escolha = input("Escolha uma opção: ")
        return escolha if escolha in opcoes else None
    
    def solicitar_alteracao_senha(self):
        print("\n=== ALTERAR SENHA ===")
        senha_atual = input("Senha atual: ")
        nova_senha = input("Nova senha: ")
        confirmar_nova = input("Confirme a nova senha: ")
        
        if nova_senha != confirmar_nova:
            print("Senhas não coincidem!")
            return None, None
        
        return senha_atual, nova_senha
    
    def mostrar_relatorio(self, relatorio):
        print("\n" + relatorio)
        input("Pressione Enter para continuar...")
    
    def mostrar_mensagem_sucesso(self, mensagem):
        print(f"✓ {mensagem}")
    
    def mostrar_mensagem_erro(self, mensagem):
        print(f"✗ {mensagem}")
    
    def confirmar_acao(self, mensagem):
        """Solicita confirmação para uma ação"""
        resposta = input(f"{mensagem} (s/n): ").lower()
        return resposta in ['s', 'sim', 'y', 'yes']