import pickle
import os

class VotoDAO:
    def __init__(self, arquivo='dados/votos.pkl'):
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

    def adicionar(self, voto):
        self.__contador_id += 1
        chave = self.__contador_id
        self.__cache[chave] = voto
        self.salvar()
        return chave

    def listar(self):
        return list(self.__cache.values())