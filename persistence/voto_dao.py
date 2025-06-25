import pickle
import os

class VotoDAO:
    def __init__(self, arquivo='dados/votos.pkl'):
        self.arquivo = arquivo
        self.votos = self.carregar()

    def salvar(self):
        os.makedirs(os.path.dirname(self.arquivo), exist_ok=True)
        with open(self.arquivo, 'wb') as f:
            pickle.dump(self.votos, f)

    def carregar(self):
        if os.path.exists(self.arquivo):
            with open(self.arquivo, 'rb') as f:
                return pickle.load(f)
        return []

    def adicionar(self, voto):
        self.votos.append(voto)
        self.salvar()

    def listar(self):
        return self.votos
