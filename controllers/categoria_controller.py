from models.categoria import Categoria
from persistence.categoria_dao import CategoriaDAO

class CategoriaController:
    def __init__(self):
        self.__dao = CategoriaDAO()
        self.__categorias = self.__dao.listar()
        self.__criar_categorias_padrao()

    def __criar_categorias_padrao(self):
        categorias_existentes = [c.nome for c in self.__dao.listar()]
        categorias_padrao = [
            "Melhor Filme",
            "Melhor Diretor",
            "Melhor Ator",
            "Melhor Atriz",
            "Melhor Ator Coadjuvante",
            "Melhor Atriz Coadjuvante"
        ]
        for nome in categorias_padrao:
            if nome not in categorias_existentes:
                categoria = Categoria(nome)
                self.__dao.adicionar(categoria)
        self.__categorias = self.__dao.listar()

    def criar_categoria(self, nome):
        try:
            categoria = Categoria(nome)
            self.__dao.adicionar(categoria)
            self.__categorias = self.__dao.listar()
            return categoria
        except Exception as e:
            return None

    def listar_categorias(self):
        return self.__dao.listar()

    def buscar_categoria(self, nome):
        return self.__dao.buscar_por_nome(nome)

    def adicionar_indicado(self, nome_categoria, indicado):
        categoria = self.__dao.buscar_por_nome(nome_categoria)
        if categoria:
            categoria.adicionar_indicado(indicado)
            self.__dao.salvar()
            return True
        return False