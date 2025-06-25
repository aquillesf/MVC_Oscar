from models.diretor import Diretor
from exceptions.item_nao_encontrado_exception import ItemNaoEncontradoException
from exceptions.dados_invalidos_exception import DadosInvalidosException

class DiretorController:
    def __init__(self):
        self.__diretores = []
    
    def criar_diretor(self, nome, idade, filmes_dirigidos):
        if not nome or not nome.strip():
            raise DadosInvalidosException("nome", nome)
        
        if not isinstance(idade, int) or idade < 0:
            raise DadosInvalidosException("idade", idade)
        
        try:
            diretor = Diretor(nome.strip(), idade, filmes_dirigidos)
            self.__diretores.append(diretor)
            return diretor
        except Exception as e:
            raise DadosInvalidosException("dados do diretor", str(e))
    
    def excluir_diretor(self, nome):
        """Exclui um diretor pelo nome"""
        diretor = self.buscar_diretor(nome)
        if not diretor:
            raise ItemNaoEncontradoException("Diretor", nome)
        
        self.__diretores.remove(diretor)
        return True
    
    def editar_diretor(self, nome_atual, novo_nome=None, nova_idade=None, novos_filmes=None):
        diretor = self.buscar_diretor(nome_atual)
        if not diretor:
            raise ItemNaoEncontradoException("Diretor", nome_atual)
        
        if novo_nome and novo_nome.strip():
            diretor._Pessoa__nome = novo_nome.strip()
        
        if nova_idade is not None and isinstance(nova_idade, int) and nova_idade >= 0:
            diretor._Pessoa__idade = nova_idade
        
        if novos_filmes is not None:
            diretor._Diretor__filmes_dirigidos = novos_filmes
        
        return diretor
    
    def listar_diretores(self):
        return self.__diretores
    
    def buscar_diretor(self, nome):
        for diretor in self.__diretores:
            if diretor.nome.lower() == nome.lower():
                return diretor
        return None
    
    def encontrar_ou_criar_diretor(self, nome):
        diretor = self.buscar_diretor(nome)
        if not diretor:
            diretor = self.criar_diretor(nome, 0, [])
        return diretor
    
    def carregar_diretores(self, diretores_list):
        self.__diretores = diretores_list