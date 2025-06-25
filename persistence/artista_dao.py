import pickle
import os

class ArtistaDAO:
    def __init__(self, arquivo='dados/artistas.pkl'):
        self.arquivo = arquivo
        self.artistas = self.carregar()

    def salvar(self):
        os.makedirs(os.path.dirname(self.arquivo), exist_ok=True)
        with open(self.arquivo, 'wb') as f:
            pickle.dump(self.artistas, f)

    def carregar(self):
        if os.path.exists(self.arquivo):
            with open(self.arquivo, 'rb') as f:
                return pickle.load(f)
        return []

    def adicionar(self, artista):
        self.artistas.append(artista)
        self.salvar()

    def listar(self):
        return self.artistas

    def buscar_por_nome(self, nome):
        for artista in self.artistas:
            if artista.nome.lower() == nome.lower():
                return artista
        return None
