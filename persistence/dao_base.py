import pickle
import os
from abc import ABC, abstractmethod

class DAOBase(ABC):
    def __init__(self, arquivo):
        self.__arquivo = arquivo
        self.__dados = []
        self.__criar_diretorio()
        self.carregar_dados()

    def __criar_diretorio(self):
        diretorio = os.path.dirname(self.__arquivo)
        if diretorio and not os.path.exists(diretorio):
            os.makedirs(diretorio)

    def salvar_dados(self):
        try:
            with open(self.__arquivo, 'wb') as arquivo:
                pickle.dump(self.__dados, arquivo)
        except Exception as e:
            raise Exception(f"Erro ao salvar dados: {str(e)}")

    def carregar_dados(self):
        try:
            if os.path.exists(self.__arquivo):
                with open(self.__arquivo, 'rb') as arquivo:
                    self.__dados = pickle.load(arquivo)
            else:
                self.__dados = []
        except Exception as e:
            self.__dados = []
            print(f"Aviso: Erro ao carregar dados de {self.__arquivo}: {str(e)}")

    def adicionar(self, objeto):
        if objeto not in self.__dados:
            self.__dados.append(objeto)
            self.salvar_dados()
            return True
        return False

    def remover(self, objeto):
        if objeto in self.__dados:
            self.__dados.remove(objeto)
            self.salvar_dados()
            return True
        return False

    def listar_todos(self):
        return self.__dados.copy()

    def limpar_dados(self):
        self.__dados = []
        self.salvar_dados()

    @abstractmethod
    def buscar_por_id(self, id):
        pass
