from models.pessoa import Pessoa
class PessoaController:
    def __init__(self):
        self.__pessoas = []
    
    def criar_pessoa(self, nome, idade):
        try:
            pessoa = Pessoa(nome, idade)
            self.__pessoas.append(pessoa)
            return pessoa
        except Exception as e:
            return None
    
    def listar_pessoas(self):
        return self.__pessoas
    
    def buscar_pessoa(self, nome):
        for pessoa in self.__pessoas:
            if pessoa.nome.lower() == nome.lower():
                return pessoa
        return None