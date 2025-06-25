import pickle
import os

class MembroDAO:
    def __init__(self, arquivo='dados/membros.pkl'):
        self.arquivo = arquivo
        self.membros = self.carregar()

    def salvar(self):
        os.makedirs(os.path.dirname(self.arquivo), exist_ok=True)
        with open(self.arquivo, 'wb') as f:
            pickle.dump(self.membros, f)

    def carregar(self):
        if os.path.exists(self.arquivo):
            with open(self.arquivo, 'rb') as f:
                return pickle.load(f)
        return []

    def adicionar(self, membro):
        self.membros.append(membro)
        self.salvar()

    def listar(self):
        return self.membros

    def buscar_por_nome(self, nome):
        for membro in self.membros:
            if membro.nome.lower() == nome.lower():
                return membro
        return None
