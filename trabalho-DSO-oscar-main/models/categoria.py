class Categoria:
    def __init__(self, nome, indicados=None):
        self.__nome = nome
        self.__indicados = indicados if indicados else []
        self.__votos = {}
    
    @property
    def nome(self):
        return self.__nome
    
    @property
    def indicados(self):
        return self.__indicados
    
    @property
    def votos(self):
        return self.__votos
    
    def adicionar_indicado(self, indicado):
        self.__indicados.append(indicado)
    
    def registrar_voto(self, indicado, membro):
        if indicado not in self.__indicados:
            return False
        if membro not in self.__votos:
            self.__votos[membro] = indicado
            return True
        return False