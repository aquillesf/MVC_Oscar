from models.diretor import Diretor
class DiretorController:
    def __init__(self):
        self.__diretores = []
    
    def criar_diretor(self, nome, idade, filmes_dirigidos):
        try:
            diretor = Diretor(nome, idade, filmes_dirigidos)
            self.__diretores.append(diretor)
            return diretor
        except Exception as e:
            return None
    
    def listar_diretores(self):
        return self.__diretores
    
    def buscar_diretor(self, nome):
        for diretor in self.__diretores:
            if diretor.nome.lower() == nome.lower():
                return diretor
        return None
    
    def encontrar_ou_criar_diretor(self, nome):
        diretor = self.buscar_diretor(nome)
        if not diretor:
            diretor = self.criar_diretor(nome, 0, [])
        return diretor