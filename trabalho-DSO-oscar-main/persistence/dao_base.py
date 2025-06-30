import pickle
import os
from abc import ABC, abstractmethod

class DAOBase(ABC):
    def __init__(self, arquivo):
        self.__arquivo = arquivo
        self.__cache = {} 
        self.__criar_diretorio()
        self.carregar_dados()

    def __criar_diretorio(self):
        diretorio = os.path.dirname(self.__arquivo)
        if diretorio and not os.path.exists(diretorio):
            os.makedirs(diretorio)

    def salvar_dados(self):
        try:
            with open(self.__arquivo, 'wb') as arquivo:
                pickle.dump(self.__cache, arquivo)
        except Exception as e:
            raise Exception(f"Erro ao salvar dados: {str(e)}")

    def carregar_dados(self):
        try:
            if os.path.exists(self.__arquivo):
                with open(self.__arquivo, 'rb') as arquivo:
                    self.__cache = pickle.load(arquivo)
            else:
                self.__cache = {}
        except Exception as e:
            self.__cache = {}
            print(f"Aviso: Erro ao carregar dados de {self.__arquivo}: {str(e)}")

    def adicionar(self, chave, objeto):
        self.__cache[chave] = objeto
        self.salvar_dados()
        return True

    def remover(self, chave):
        if chave in self.__cache:
            del self.__cache[chave]
            self.salvar_dados()
            return True
        return False

    def buscar(self, chave):
        return self.__cache.get(chave)

    def listar_todos(self):
        return list(self.__cache.values())

    def listar_chaves(self):
        return list(self.__cache.keys())

    def limpar_dados(self):
        self.__cache = {}
        self.salvar_dados()

    def existe(self, chave):
        return chave in self.__cache

    @abstractmethod
    def buscar_por_id(self, id):
        pass