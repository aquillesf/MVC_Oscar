# categoria.py
class Categoria:
    def __init__(self, nome, indicados=None):
        self.nome = nome
        self.indicados = indicados if indicados else []
        self.votos = {}

    def adicionar_indicado(self, indicado):
        self.indicados.append(indicado)

    def registrar_voto(self, indicado, membro):
        if indicado not in self.indicados:
            return False
        if membro not in self.votos:
            self.votos[membro] = indicado
            return True
        return False
