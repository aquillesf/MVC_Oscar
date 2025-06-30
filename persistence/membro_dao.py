import pickle
import os

class MembroDAO:
    def __init__(self, arquivo='dados/membros.pkl'):
        self.arquivo = arquivo
        self.__cache = {}  
        self.carregar()

    def salvar(self):
        os.makedirs(os.path.dirname(self.arquivo), exist_ok=True)
        with open(self.arquivo, 'wb') as f:
            pickle.dump(self.__cache, f)

    def carregar(self):
        if os.path.exists(self.arquivo):
            try:
                with open(self.arquivo, 'rb') as f:
                    self.__cache = pickle.load(f)
            except:
                self.__cache = {}
        else:
            self.__cache = {}

    def adicionar(self, membro):
        chave = membro.nome.lower()
        self.__cache[chave] = membro
        self.salvar()

    def listar(self):
        return list(self.__cache.values())

    def buscar_por_nome(self, nome):
        return self.__cache.get(nome.lower())

    def remover(self, membro):
        chave = membro.nome.lower()
        if chave in self.__cache:
            del self.__cache[chave]
            self.salvar()
            return True
        return False