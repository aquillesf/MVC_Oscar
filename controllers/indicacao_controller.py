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
    
    def deletar_indicacao(self, nome_categoria, indicado):
        try:
            categoria = self.__categoria_controller.buscar_categoria(nome_categoria)
            if not categoria:
                return False
            
            indicacao_para_remover = None
            for indicacao in self.__indicacoes:
                if indicacao.categoria == categoria and indicacao.indicado == indicado:
                    indicacao_para_remover = indicacao
                    break
            
            if indicacao_para_remover:
                self.__indicacoes.remove(indicacao_para_remover)

                if hasattr(categoria, 'remover_indicado'):
                    categoria.remover_indicado(indicado)
                elif hasattr(categoria, '_Categoria__indicados'):
                    if indicado in categoria._Categoria__indicados:
                        categoria._Categoria__indicados.remove(indicado)
                
                return True
            
            return False
            
        except Exception as e:
            print(f"Erro ao deletar indicação: {str(e)}")
            return False