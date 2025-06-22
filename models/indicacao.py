class Indicacao:
    def __init__(self, categoria, indicado):
        self.__categoria = categoria
        self.__indicado = indicado
    
    @property
    def categoria(self):
        return self.__categoria
    
    @property
    def indicado(self):
        return self.__indicado