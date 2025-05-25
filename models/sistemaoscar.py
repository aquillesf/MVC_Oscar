from models.membro import Membro
from models.categoria import Categoria
from models.filme import Filme
from models.diretor import Diretor
from models.ator import Ator
from models.indicacao import Indicacao
from models.voto import Voto

class SistemaOscar:
    def __init__(self):
        self.__membros = []
        self.__categorias = []
        self.__filmes = []
        self.__diretores = []
        self.__atores = []
        self.__indicacoes = []
        self.__votos = []

        categorias_padrao = [
            "Melhor Filme",
            "Melhor Diretor", 
            "Melhor Ator",
            "Melhor Atriz",
            "Melhor Ator Coadjuvante",
            "Melhor Atriz Coadjuvante"
        ]
        
        for nome_categoria in categorias_padrao:
            self.__categorias.append(Categoria(nome_categoria))
    
    @property
    def membros(self):
        return self.__membros
    
    @property
    def categorias(self):
        return self.__categorias
    
    @property
    def filmes(self):
        return self.__filmes
    
    @property
    def diretores(self):
        return self.__diretores
    
    @property
    def atores(self):
        return self.__atores
    
    @property
    def indicacoes(self):
        return self.__indicacoes
    
    @property
    def votos(self):
        return self.__votos