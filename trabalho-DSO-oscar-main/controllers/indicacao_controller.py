from models.indicacao import Indicacao
from persistence.indicacao_dao import IndicacaoDAO

class IndicacaoController:
    def __init__(self, categoria_controller):
        self.__dao = IndicacaoDAO()
        self.__indicacoes = self.__dao.listar()
        self.__categoria_controller = categoria_controller

    def criar_indicacao(self, nome_categoria, indicado):
        categoria = self.__categoria_controller.buscar_categoria(nome_categoria)
        if not categoria:
            return None
        try:
            indicacao = Indicacao(categoria, indicado)
            self.__dao.adicionar(indicacao)
            categoria.adicionar_indicado(indicado)
            self.__indicacoes = self.__dao.listar()
            return indicacao
        except Exception as e:
            return None

    def listar_indicacoes(self):
        return self.__dao.listar()

    def listar_por_categoria(self, categoria):
        return [i for i in self.__dao.listar() if i.categoria == categoria]

    def deletar_indicacao(self, nome_categoria, indicado):
        try:
            categoria = self.__categoria_controller.buscar_categoria(nome_categoria)
            if not categoria:
                return False
            indicacao_para_remover = None
            for indicacao in self.__dao.listar():
                if indicacao.categoria == categoria and indicacao.indicado == indicado:
                    indicacao_para_remover = indicacao
                    break
            if indicacao_para_remover:
                self.__dao.remover(indicacao_para_remover)
                if hasattr(categoria, 'remover_indicado'):
                    categoria.remover_indicado(indicado)
                elif hasattr(categoria, '_Categoria__indicados'):
                    if indicado in categoria._Categoria__indicados:
                        categoria._Categoria__indicados.remove(indicado)
                self.__indicacoes = self.__dao.listar()
                return True
            return False
        except Exception as e:
            print(f"Erro ao deletar indicação: {str(e)}")
            return False
