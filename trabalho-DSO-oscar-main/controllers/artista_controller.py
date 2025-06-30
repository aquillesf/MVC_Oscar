from models.artista import Artista
from persistence.artista_dao import ArtistaDAO

class ArtistaController:
    def __init__(self):
        self.__dao = ArtistaDAO()
        self.__cache_por_nacionalidade = {}
        self.__atualizar_cache_nacionalidade()

    def __atualizar_cache_nacionalidade(self):
        self.__cache_por_nacionalidade = {}
        for artista in self.__dao.listar():
            nacionalidade_lower = artista.nacionalidade.lower()
            if nacionalidade_lower not in self.__cache_por_nacionalidade:
                self.__cache_por_nacionalidade[nacionalidade_lower] = []
            self.__cache_por_nacionalidade[nacionalidade_lower].append(artista)

    def criar_artista(self, nome, idade, filmes_participados, nacionalidade):
        try:
            artista = Artista(nome, idade, filmes_participados, nacionalidade)
            self.__dao.adicionar(artista)
            self.__atualizar_cache_nacionalidade()
            return artista
        except Exception as e:
            return None

    def listar_artistas(self):
        return self.__dao.listar()

    def buscar_artista(self, nome):
        return self.__dao.buscar_por_nome(nome)

    def listar_por_nacionalidade(self, nacionalidade):
        return self.__cache_por_nacionalidade.get(nacionalidade.lower(), [])