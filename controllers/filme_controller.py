from models.filme import Filme
class FilmeController:
    def __init__(self, diretor_controller):
        self.__filmes = []
        self.__diretor_controller = diretor_controller
    
    def criar_filme(self, titulo, ano, genero, diretor_nome, descricao=""):
        try:
            diretor = self.__diretor_controller.encontrar_ou_criar_diretor(diretor_nome)
            filme = Filme(titulo, ano, genero, diretor, descricao)
            self.__filmes.append(filme)
            return filme
        except Exception as e:
            return None
    
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