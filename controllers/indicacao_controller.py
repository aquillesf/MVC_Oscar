from models.indicacao import Indicacao
class IndicacaoController:
    def __init__(self, categoria_controller):
        self.__indicacoes = []
        self.__categoria_controller = categoria_controller
    
    def criar_indicacao(self, nome_categoria, indicado):
        categoria = self.__categoria_controller.buscar_categoria(nome_categoria)
        if not categoria:
            return None
        
        try:
            indicacao = Indicacao(categoria, indicado)
            self.__indicacoes.append(indicacao)
            categoria.adicionar_indicado(indicado)
            return indicacao
        except Exception as e:
            return None
    
    def listar_indicacoes(self):
        return self.__indicacoes
    
    def listar_por_categoria(self, categoria):
        return [i for i in self.__indicacoes if i.categoria == categoria]