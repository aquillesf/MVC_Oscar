from models.categoria import Categoria
class CategoriaController:
    def __init__(self):
        self.__categorias = []
        self.__criar_categorias_padrao()
    
    def __criar_categorias_padrao(self):
        categorias_padrao = [
            "Melhor Filme",
            "Melhor Diretor",
            "Melhor Ator", 
            "Melhor Atriz",
            "Melhor Ator Coadjuvante",
            "Melhor Atriz Coadjuvante"
        ]
        
        for nome in categorias_padrao:
            self.__categorias.append(Categoria(nome))
    
    def criar_categoria(self, nome):
        try:
            categoria = Categoria(nome)
            self.__categorias.append(categoria)
            return categoria
        except Exception as e:
            return None
    
    def listar_categorias(self):
        return self.__categorias
    
    def buscar_categoria(self, nome):
        for categoria in self.__categorias:
            if categoria.nome.lower() == nome.lower():
                return categoria
        return None
    
    def adicionar_indicado(self, nome_categoria, indicado):
        categoria = self.buscar_categoria(nome_categoria)
        if categoria:
            categoria.adicionar_indicado(indicado)
            return True
        return False
