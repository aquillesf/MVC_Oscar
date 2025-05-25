from models.ator import Ator
class AtorController:
    def __init__(self):
        self.__atores = []
    
    def criar_ator(self, nome, idade, filmes_participados, tipo_ator, nacionalidade="Desconhecida"):
        try:
            ator = Ator(nome, idade, filmes_participados, tipo_ator, nacionalidade)
            self.__atores.append(ator)
            return ator
        except Exception as e:
            return None
    
    def listar_atores(self):
        return self.__atores
    
    def buscar_ator(self, nome):
        for ator in self.__atores:
            if ator.nome.lower() == nome.lower():
                return ator
        return None
    
    def listar_por_tipo(self, tipo):
        return [a for a in self.__atores if a.tipo_ator.lower() == tipo.lower()]