from models.pessoa import Pessoa

class Diretor(Pessoa):
    def __init__(self, nome, idade, filmes_dirigidos):
        super().__init__(nome, idade)
        self.filmes_dirigidos = filmes_dirigidos
