from models.artista import Artista
from persistence.artista_dao import ArtistaDAO

class ArtistaController:
    def __init__(self):
        self.__dao = ArtistaDAO()
        self.__artistas = self.__dao.listar()

    def criar_artista(self, nome, idade, filmes_participados, nacionalidade):
        try:
            artista = Artista(nome, idade, filmes_participados, nacionalidade)
            self.__dao.adicionar(artista)
            self.__artistas = self.__dao.listar()
            return artista
        except Exception as e:
            return None

    def listar_artistas(self):
        return self.__dao.listar()

    def buscar_artista(self, nome):
        return self.__dao.buscar_por_nome(nome)

    def listar_por_nacionalidade(self, nacionalidade):
        return [a for a in self.__dao.listar() if a.nacionalidade.lower() == nacionalidade.lower()]
