import pickle
import os

class DiretorDAO:
    def __init__(self, arquivo='dados/diretores.pkl'):
        self.arquivo = arquivo
        self.diretores = self.carregar()

    def salvar(self):
        os.makedirs(os.path.dirname(self.arquivo), exist_ok=True)
        with open(self.arquivo, 'wb') as f:
            pickle.dump(self.diretores, f)

    def carregar(self):
        if os.path.exists(self.arquivo):
            with open(self.arquivo, 'rb') as f:
                return pickle.load(f)
        return []

    def adicionar(self, diretor):
        self.diretores.append(diretor)
        self.salvar()

    def remover(self, diretor):
        self.diretores.remove(diretor)
        self.salvar()

    def listar(self):
        return self.diretores

    def buscar_por_nome(self, nome):
        for diretor in self.diretores:
            if diretor.nome.lower() == nome.lower():
                return diretor
        return None
