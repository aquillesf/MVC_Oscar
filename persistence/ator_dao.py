import pickle
import os

class AtorDAO:
    def __init__(self, arquivo='dados/atores.pkl'):
        self.arquivo = arquivo
        self.atores = self.carregar()

    def salvar(self):
        os.makedirs(os.path.dirname(self.arquivo), exist_ok=True)
        with open(self.arquivo, 'wb') as f:
            pickle.dump(self.atores, f)

    def carregar(self):
        if os.path.exists(self.arquivo):
            with open(self.arquivo, 'rb') as f:
                return pickle.load(f)
        return []

    def adicionar(self, ator):
        self.atores.append(ator)
        self.salvar()

    def remover(self, ator):
        self.atores.remove(ator)
        self.salvar()

    def listar(self):
        return self.atores

    def buscar_por_nome(self, nome):
        for ator in self.atores:
            if ator.nome.lower() == nome.lower():
                return ator
        return None
