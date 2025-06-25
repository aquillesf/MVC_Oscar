import pickle
import os

class IndicacaoDAO:
    def __init__(self, arquivo='dados/indicacoes.pkl'):
        self.arquivo = arquivo
        self.indicacoes = self.carregar()

    def salvar(self):
        os.makedirs(os.path.dirname(self.arquivo), exist_ok=True)
        with open(self.arquivo, 'wb') as f:
            pickle.dump(self.indicacoes, f)

    def carregar(self):
        if os.path.exists(self.arquivo):
            with open(self.arquivo, 'rb') as f:
                return pickle.load(f)
        return []

    def adicionar(self, indicacao):
        self.indicacoes.append(indicacao)
        self.salvar()

    def remover(self, indicacao):
        self.indicacoes.remove(indicacao)
        self.salvar()

    def listar(self):
        return self.indicacoes
