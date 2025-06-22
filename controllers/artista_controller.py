from models.artista import Artista
class ArtistaController:
    def __init__(self):
        self.__artistas = []
    
    def criar_artista(self, nome, idade, filmes_participados, nacionalidade):
        try:
            artista = Artista(nome, idade, filmes_participados, nacionalidade)
            self.__artistas.append(artista)
            return artista
        except Exception as e:
            return None
    
    def listar_artistas(self):
        return self.__artistas
    
    def buscar_artista(self, nome):
        for artista in self.__artistas:
            if artista.nome.lower() == nome.lower():
                return artista
        return None
    
    def listar_por_nacionalidade(self, nacionalidade):
        return [a for a in self.__artistas if a.nacionalidade.lower() == nacionalidade.lower()]