# models/membro.py
class Membro:
    TIPOS = {'VOTADOR', 'REGISTRADOR'}
    
    def __init__(self, nome, tipo, senha):
        self.__nome = nome
        if tipo not in self.TIPOS:
            raise ValueError("Tipo de membro inválido")
        self.__tipo = tipo
        self.__senha = senha
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
    
    def verificar_senha(self, senha):
        return self.__senha == senha
    
    def alterar_senha(self, senha_atual, nova_senha):
        if self.verificar_senha(senha_atual):
            self.__senha = nova_senha
            return True
        return False
    
    def pode_votar(self):
        return self.__tipo == 'VOTADOR'
    
    def pode_registrar(self):
        return self.__tipo == 'REGISTRADOR'