from models.filme import Filme
from exceptions.oscar_exceptions import ItemNaoEncontradoException, DadosInvalidosException

class FilmeController:
    def __init__(self, diretor_controller):
        self.__filmes = []
        self.__diretor_controller = diretor_controller
    
    def criar_filme(self, titulo, ano, genero, diretor_nome, descricao=""):
        if not titulo or not titulo.strip():
            raise DadosInvalidosException("título", titulo)
        
        if not isinstance(ano, int) or ano < 1900 or ano > 2030:
            raise DadosInvalidosException("ano", ano)
        
        try:
            diretor = self.__diretor_controller.encontrar_ou_criar_diretor(diretor_nome)
            filme = Filme(titulo.strip(), ano, genero.strip(), diretor, descricao.strip())
            self.__filmes.append(filme)
            return filme
        except Exception as e:
            raise DadosInvalidosException("dados do filme", str(e))
    
    def excluir_filme(self, titulo):
        """Exclui um filme pelo título"""
        filme = self.buscar_filme(titulo)
        if not filme:
            raise ItemNaoEncontradoException("Filme", titulo)
        
        self.__filmes.remove(filme)
        return True
    
    def editar_filme(self, titulo_atual, novo_titulo=None, novo_ano=None, novo_genero=None, nova_descricao=None):
        """Edita dados de um filme"""
        filme = self.buscar_filme(titulo_atual)
        if not filme:
            raise ItemNaoEncontradoException("Filme", titulo_atual)
        
        if novo_titulo and novo_titulo.strip():
            filme._Filme__titulo = novo_titulo.strip()
        
        if novo_ano and isinstance(novo_ano, int) and 1900 <= novo_ano <= 2030:
            filme._Filme__ano = novo_ano
        
        if novo_genero and novo_genero.strip():
            filme._Filme__genero = novo_genero.strip()
        
        if nova_descricao is not None:
            filme._Filme__descricao = nova_descricao.strip()
        
        return filme
    
    def listar_filmes(self):
        return self.__filmes
    
    def buscar_filme(self, titulo):
        for filme in self.__filmes:
            if filme.titulo.lower() == titulo.lower():
                return filme
        return None
    
    def listar_por_ano(self, ano):
        return [f for f in self.__filmes if f.ano == ano]
    
    def listar_por_genero(self, genero):
        return [f for f in self.__filmes if f.genero.lower() == genero.lower()]
    
    def carregar_filmes(self, filmes_list):
        """Carrega lista de filmes (usado pela persistência)"""
        self.__filmes = filmes_list