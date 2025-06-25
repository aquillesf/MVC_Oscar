import pickle
import os

class PessoaDAO:
    def __init__(self, arquivo='dados/pessoas.pkl'):
        self.arquivo = arquivo
        self.pessoas = self.carregar()

    def salvar(self):
        os.makedirs(os.path.dirname(self.arquivo), exist_ok=True)
        with open(self.arquivo, 'wb') as f:
            pickle.dump(self.pessoas, f)

    def carregar(self):
        if os.path.exists(self.arquivo):
            with open(self.arquivo, 'rb') as f:
                return pickle.load(f)
        return []

    def adicionar(self, pessoa):
        self.pessoas.append(pessoa)
        self.salvar()

    def listar(self):
        return self.pessoas

    def buscar_por_nome(self, nome):
        for pessoa in self.pessoas:
            if pessoa.nome.lower() == nome.lower():
                return pessoa
        return None
