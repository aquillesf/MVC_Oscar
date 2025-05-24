from models.artista import Artista

class Ator(Artista):
    def __init__(self, nome, idade, filmes_participados, tipo_ator, nacionalidade="Desconhecida"):
        super().__init__(nome, idade, filmes_participados, nacionalidade)
        self.tipo_ator = tipo_ator