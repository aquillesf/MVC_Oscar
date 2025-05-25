class Filme:
    def __init__(self, titulo, ano, genero, diretor, descricao=""):
        self.__titulo = titulo
        self.__ano = ano
        self.__genero = genero
        self.__diretor = diretor
        self.__descricao = descricao
    
    @property
    def titulo(self):
        return self.__titulo
    
    @property
    def ano(self):
        return self.__ano
    
    @property
    def genero(self):
        return self.__genero
    
    @property
    def diretor(self):
        return self.__diretor
    
    @property
    def descricao(self):
        return self.__descricao
