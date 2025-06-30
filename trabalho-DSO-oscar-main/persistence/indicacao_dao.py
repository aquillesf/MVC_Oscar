import pickle
import os

class IndicacaoDAO:
    def __init__(self, arquivo='dados/indicacoes.pkl'):
        self.arquivo = arquivo
        self.__cache = {}  
        self.__contador_id = 0
        self.carregar()

    def salvar(self):
        os.makedirs(os.path.dirname(self.arquivo), exist_ok=True)
        dados = {
            'cache': self.__cache,
            'contador_id': self.__contador_id
        }
        with open(self.arquivo, 'wb') as f:
            pickle.dump(dados, f)

    def carregar(self):
        if os.path.exists(self.arquivo):
            try:
                with open(self.arquivo, 'rb') as f:
                    dados = pickle.load(f)
                    if isinstance(dados, dict) and 'cache' in dados:
                        self.__cache = dados['cache']
                        self.__contador_id = dados.get('contador_id', 0)
                    else:
                        self.__cache = {}
                        self.__contador_id = 0
            except:
                self.__cache = {}
                self.__contador_id = 0
        else:
            self.__cache = {}
            self.__contador_id = 0

    def adicionar(self, indicacao):
        self.__contador_id += 1
        chave = self.__contador_id
        self.__cache[chave] = indicacao
        self.salvar()
        return chave

    def remover(self, indicacao):
        chave_para_remover = None
        for chave, ind in self.__cache.items():
            if ind == indicacao:
                chave_para_remover = chave
                break
        
        if chave_para_remover:
            del self.__cache[chave_para_remover]
            self.salvar()
            return True
        return False

    def listar(self):
        return list(self.__cache.values())