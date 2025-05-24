from models.pessoa import Pessoa

class Artista(Pessoa):
    def __init__(self, nome, idade, filmes_participados, nacionalidade):
        super().__init__(nome, idade)
        self.filmes_participados = filmes_participados
        self.nacionalidade = nacionalidade