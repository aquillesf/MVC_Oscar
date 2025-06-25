from models.membro import Membro
from exceptions.membro_ja_existente_exception import MembroJaExistenteException
from exceptions.membro_nao_encontrado_exception import MembroNaoEncontradoException
from exceptions.senha_incorreta_exception import SenhaIncorretaException
from exceptions.dados_invalidos_exception import DadosInvalidosException
from persistence.membro_dao import MembroDAO

class MembroController:
    def __init__(self):
        self.__dao = MembroDAO()
        self.__membros = self.__dao.listar()

    def criar_membro(self, nome, tipo, senha):
        if not nome or not nome.strip():
            raise DadosInvalidosException("nome", nome)
        if self.__dao.buscar_por_nome(nome):
            raise MembroJaExistenteException(nome)
        try:
            membro = Membro(nome.strip(), tipo, senha)
            self.__dao.adicionar(membro)
            self.__membros = self.__dao.listar()
            return membro
        except ValueError as e:
            raise DadosInvalidosException("tipo de membro", tipo)

    def editar_membro(self, nome_atual, novo_nome=None, novo_tipo=None):
        membro = self.__dao.buscar_por_nome(nome_atual)
        if not membro:
            raise MembroNaoEncontradoException(nome_atual)
        if novo_nome and novo_nome.strip() and novo_nome != nome_atual:
            if self.__dao.buscar_por_nome(novo_nome):
                raise MembroJaExistenteException(novo_nome)
            membro._Membro__nome = novo_nome.strip()
        if novo_tipo and novo_tipo in Membro.TIPOS:
            membro._Membro__tipo = novo_tipo
        self.__dao.salvar()
        return membro

    def listar_membros(self):
        return self.__dao.listar()

    def buscar_membro(self, nome):
        return self.__dao.buscar_por_nome(nome)

    def autenticar(self, nome, senha):
        membro = self.__dao.buscar_por_nome(nome)
        if not membro:
            raise MembroNaoEncontradoException(nome)
        if not membro.verificar_senha(senha):
            raise SenhaIncorretaException()
        return membro

    def alterar_senha_membro(self, nome, senha_atual, nova_senha):
        membro = self.__dao.buscar_por_nome(nome)
        if not membro:
            raise MembroNaoEncontradoException(nome)
        if not membro.alterar_senha(senha_atual, nova_senha):
            raise SenhaIncorretaException()
        self.__dao.salvar()
        return True

    def listar_por_tipo(self, tipo):
        return [m for m in self.__dao.listar() if m.tipo == tipo]

