import pickle
import os

class CategoriaDAO:
    def __init__(self, arquivo='dados/categorias.pkl'):
        self.arquivo = arquivo
        self.categorias = self.carregar()

    def salvar(self):
        os.makedirs(os.path.dirname(self.arquivo), exist_ok=True)
        with open(self.arquivo, 'wb') as f:
            pickle.dump(self.categorias, f)

    def carregar(self):
        if os.path.exists(self.arquivo):
            with open(self.arquivo, 'rb') as f:
                return pickle.load(f)
        return []

    def adicionar(self, categoria):
        self.categorias.append(categoria)
        self.salvar()

    def listar(self):
        return self.categorias

    def buscar_por_nome(self, nome):
        for categoria in self.categorias:
            if categoria.nome.lower() == nome.lower():
                return categoria
        return None
