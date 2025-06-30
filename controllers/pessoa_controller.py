from models.pessoa import Pessoa
from persistence.pessoa_dao import PessoaDAO

class PessoaController:
    def __init__(self):
        self.__dao = PessoaDAO()
        self.__pessoas = self.__dao.listar()

    def criar_pessoa(self, nome, idade):
        try:
            pessoa = Pessoa(nome, idade)
            self.__dao.adicionar(pessoa)
            self.__pessoas = self.__dao.listar()
            return pessoa
        except Exception as e:
            return None

    def listar_pessoas(self):
        return self.__dao.listar()

    def buscar_pessoa(self, nome):
        return self.__dao.buscar_por_nome(nome)