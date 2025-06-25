from models.ator import Ator
from exceptions.item_nao_encontrado_exception import ItemNaoEncontradoException
from exceptions.dados_invalidos_exception import DadosInvalidosException
from persistence.ator_dao import AtorDAO

class AtorController:
    def __init__(self):
        self.__dao = AtorDAO()
        self.__atores = self.__dao.listar()

    def criar_ator(self, nome, idade, filmes_participados, tipo_ator, nacionalidade="Desconhecida"):
        if not nome or not nome.strip():
            raise DadosInvalidosException("nome", nome)
        if not isinstance(idade, int) or idade < 0:
            raise DadosInvalidosException("idade", idade)
        try:
            ator = Ator(nome.strip(), idade, filmes_participados, tipo_ator, nacionalidade)
            self.__dao.adicionar(ator)
            self.__atores = self.__dao.listar()
            return ator
        except Exception as e:
            raise DadosInvalidosException("dados do ator", str(e))

    def excluir_ator(self, nome):
        ator = self.__dao.buscar_por_nome(nome)
        if not ator:
            raise ItemNaoEncontradoException("Ator", nome)
        self.__dao.remover(ator)
        self.__atores = self.__dao.listar()
        return True

    def editar_ator(self, nome_atual, novo_nome=None, nova_idade=None, novos_filmes=None, novo_tipo=None, nova_nacionalidade=None):
        ator = self.__dao.buscar_por_nome(nome_atual)
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
        self.__dao.salvar()
        return ator

    def listar_atores(self):
        return self.__dao.listar()

    def buscar_ator(self, nome):
        return self.__dao.buscar_por_nome(nome)

    def listar_por_tipo(self, tipo):
        return [a for a in self.__dao.listar() if a.tipo_ator.lower() == tipo.lower()]

