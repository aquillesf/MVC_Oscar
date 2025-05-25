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
    
    def mostrar_menu_logado(self, membro):
        print("\n=== MENU PRINCIPAL ===")
        
        opcoes = []
        if membro.pode_registrar():
            print("1. Adicionar Filme")
            print("2. Adicionar Ator/Atriz")
            print("3. Adicionar Indicação")
            opcoes.extend(['1', '2', '3'])
        
        if membro.pode_votar():
            print("4. Votar em uma categoria")
            opcoes.append('4')
        
        print("5. Gerar relatório")
        print("6. Logout")
        opcoes.extend(['5', '6'])
        
        return input("Escolha uma opção: ")
    
    def mostrar_relatorio(self, relatorio):
        print("\n" + relatorio)
        input("Pressione Enter para continuar...")
    
    def mostrar_mensagem_sucesso(self, mensagem):
        print(f"✓ {mensagem}")
    
    def mostrar_mensagem_erro(self, mensagem):
        print(f"✗ {mensagem}")