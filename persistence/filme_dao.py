import pickle
import os

class FilmeDAO:
    def __init__(self, arquivo='dados/filmes.pkl'):
        self.arquivo = arquivo
        self.filmes = self.carregar()

    def salvar(self):
        os.makedirs(os.path.dirname(self.arquivo), exist_ok=True)
        with open(self.arquivo, 'wb') as f:
            pickle.dump(self.filmes, f)

    def carregar(self):
        if os.path.exists(self.arquivo):
            with open(self.arquivo, 'rb') as f:
                return pickle.load(f)
        return []

    def adicionar(self, filme):
        self.filmes.append(filme)
        self.salvar()

    def remover(self, filme):
        self.filmes.remove(filme)
        self.salvar()

    def listar(self):
        return self.filmes

    def buscar_por_titulo(self, titulo):
        for filme in self.filmes:
            if filme.titulo.lower() == titulo.lower():
                return filme
        return None
