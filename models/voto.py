class Voto:
    def __init__(self, membro, categoria, indicado):
        self.__membro = membro
        self.__categoria = categoria
        self.__indicado = indicado
    
    @property
    def membro(self):
        return self.__membro
    
    @property
    def categoria(self):
        return self.__categoria
    
    @property
    def indicado(self):
        return self.__indicado