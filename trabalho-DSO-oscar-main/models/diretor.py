from models.pessoa import Pessoa

class Diretor(Pessoa):
    def __init__(self, nome, idade, filmes_dirigidos):
        super().__init__(nome, idade)
        self.__filmes_dirigidos = filmes_dirigidos
    
    @property
    def filmes_dirigidos(self):
        return self.__filmes_dirigidos