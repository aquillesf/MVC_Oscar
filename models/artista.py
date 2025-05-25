from models.pessoa import Pessoa

class Artista(Pessoa):
    def __init__(self, nome, idade, filmes_participados, nacionalidade):
        super().__init__(nome, idade)
        self.__filmes_participados = filmes_participados
        self.__nacionalidade = nacionalidade
    
    @property
    def filmes_participados(self):
        return self.__filmes_participados
    
    @property
    def nacionalidade(self):
        return self.__nacionalidade
