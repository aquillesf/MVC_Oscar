from models.filme import Filme
from exceptions.item_nao_encontrado_exception import ItemNaoEncontradoException
from exceptions.dados_invalidos_exception import DadosInvalidosException
from persistence.filme_dao import FilmeDAO

class FilmeController:
    def __init__(self, diretor_controller):
        self.__dao = FilmeDAO()
        self.__diretor_controller = diretor_controller
        self.__cache_por_ano = {}
        self.__cache_por_genero = {}
        self.__atualizar_caches()

    def __atualizar_caches(self):
        self.__cache_por_ano = {}
        self.__cache_por_genero = {}
        
        for filme in self.__dao.listar():
            if filme.ano not in self.__cache_por_ano:
                self.__cache_por_ano[filme.ano] = []
            self.__cache_por_ano[filme.ano].append(filme)
            
            genero_lower = filme.genero.lower()
            if genero_lower not in self.__cache_por_genero:
                self.__cache_por_genero[genero_lower] = []
            self.__cache_por_genero[genero_lower].append(filme)

    def criar_filme(self, titulo, ano, genero, diretor_nome, descricao=""):
        if not titulo or not titulo.strip():
            raise DadosInvalidosException("título", titulo)
        if not isinstance(ano, int) or ano < 1900 or ano > 2030:
            raise DadosInvalidosException("ano", ano)
        try:
            diretor = self.__diretor_controller.encontrar_ou_criar_diretor(diretor_nome)
            filme = Filme(titulo.strip(), ano, genero.strip(), diretor, descricao.strip())
            self.__dao.adicionar(filme)
            self.__atualizar_caches()
            return filme
        except Exception as e:
            raise DadosInvalidosException("dados do filme", str(e))

    def excluir_filme(self, titulo):
        filme = self.__dao.buscar_por_titulo(titulo)
        if not filme:
            raise ItemNaoEncontradoException("Filme", titulo)
        self.__dao.remover(filme)
        self.__atualizar_caches()
        return True

    def editar_filme(self, titulo_atual, novo_titulo=None, novo_ano=None, novo_genero=None, novo_diretor_nome=None, nova_descricao=None):
        filme = self.__dao.buscar_por_titulo(titulo_atual)
        if not filme:
            raise ItemNaoEncontradoException("Filme", titulo_atual)
        
        if novo_titulo and novo_titulo.strip():
            if novo_titulo.strip().lower() != titulo_atual.lower():
                self.__dao.remover(filme)
                filme._Filme__titulo = novo_titulo.strip()
                self.__dao.adicionar(filme)
            else:
                filme._Filme__titulo = novo_titulo.strip()
        
        if novo_ano and isinstance(novo_ano, int) and 1900 <= novo_ano <= 2030:
            filme._Filme__ano = novo_ano
        
        if novo_genero and novo_genero.strip():
            filme._Filme__genero = novo_genero.strip()
        
        if novo_diretor_nome and novo_diretor_nome.strip():
            novo_diretor = self.__diretor_controller.encontrar_ou_criar_diretor(novo_diretor_nome)
            filme._Filme__diretor = novo_diretor
        
        if nova_descricao is not None:
            filme._Filme__descricao = nova_descricao.strip()
        
        self.__dao.salvar()
        self.__atualizar_caches()
        return filme

    def listar_filmes(self):
        return self.__dao.listar()

    def buscar_filme(self, titulo):
        return self.__dao.buscar_por_titulo(titulo)

    def listar_por_ano(self, ano):
        return self.__cache_por_ano.get(ano, [])

    def listar_por_genero(self, genero):
        return self.__cache_por_genero.get(genero.lower(), [])

    def carregar_filmes(self, filmes_list):
        pass