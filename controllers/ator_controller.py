from models.ator import Ator
from exceptions.oscar_exceptions import ItemNaoEncontradoException, DadosInvalidosException

class AtorController:
    def __init__(self):
        self.__atores = []
    
    def criar_ator(self, nome, idade, filmes_participados, tipo_ator, nacionalidade="Desconhecida"):
        if not nome or not nome.strip():
            raise DadosInvalidosException("nome", nome)
        
        if not isinstance(idade, int) or idade < 0:
            raise DadosInvalidosException("idade", idade)
        
        try:
            ator = Ator(nome.strip(), idade, filmes_participados, tipo_ator, nacionalidade)
            self.__atores.append(ator)
            return ator
        except Exception as e:
            raise DadosInvalidosException("dados do ator", str(e))
    
    def excluir_ator(self, nome):
        ator = self.buscar_ator(nome)
        if not ator:
            raise ItemNaoEncontradoException("Ator", nome)
        
        self.__atores.remove(ator)
        return True
    
    def editar_ator(self, nome_atual, novo_nome=None, nova_idade=None, novos_filmes=None, novo_tipo=None, nova_nacionalidade=None):
        ator = self.buscar_ator(nome_atual)
        if not ator:
            raise ItemNaoEncontradoException("Ator", nome_atual)
        
        if novo_nome and novo_nome.strip():
            ator._Pessoa__nome = novo_nome.strip()
        
        if nova_idade is not None and isinstance(nova_idade, int) and nova_idade >= 0:
            ator._Pessoa__idade = nova_idade
        
        if novos_filmes is not None:
            ator._Artista__filmes_participados = novos_filmes
        
        if novo_tipo and novo_tipo.strip():
            ator._Ator__tipo_ator = novo_tipo.strip()
        
        if nova_nacionalidade and nova_nacionalidade.strip():
            ator._Artista__nacionalidade = nova_nacionalidade.strip()
        
        return ator
    
    def listar_atores(self):
        return self.__atores
    
    def buscar_ator(self, nome):
        for ator in self.__atores:
            if ator.nome.lower() == nome.lower():
                return ator
        return None
    
    def listar_por_tipo(self, tipo):
        return [a for a in self.__atores if a.tipo_ator.lower() == tipo.lower()]
    
    def carregar_atores(self, atores_list):
        self.__atores = atores_list