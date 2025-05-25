class Membro:
    TIPOS = {'VOTADOR', 'REGISTRADOR'}
    
    def __init__(self, nome, tipo):
        self.__nome = nome
        if tipo not in self.TIPOS:
            raise ValueError("Tipo de membro inválido")
        self.__tipo = tipo
        self.__votos_realizados = []
    
    @property
    def nome(self):
        return self.__nome
    
    @property
    def tipo(self):
        return self.__tipo
    
    @property
    def votos_realizados(self):
        return self.__votos_realizados
    
    def pode_votar(self):
        return self.__tipo == 'VOTADOR'
    
    def pode_registrar(self):
        return self.__tipo == 'REGISTRADOR'
