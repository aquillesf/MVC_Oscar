from models.membro import Membro
from exceptions.oscar_exceptions import (
    MembroJaExistenteException, MembroNaoEncontradoException, 
    SenhaIncorretaException, DadosInvalidosException
)

class MembroController:
    def __init__(self):
        self.__membros = []
    
    def criar_membro(self, nome, tipo, senha):
        if not nome or not nome.strip():
            raise DadosInvalidosException("nome", nome)
        
        if self.buscar_membro(nome):
            raise MembroJaExistenteException(nome)
        
        try:
            membro = Membro(nome.strip(), tipo, senha)
            self.__membros.append(membro)
            return membro
        except ValueError as e:
            raise DadosInvalidosException("tipo de membro", tipo)
    
    def excluir_membro(self, nome):
        """Exclui um membro pelo nome"""
        membro = self.buscar_membro(nome)
        if not membro:
            raise MembroNaoEncontradoException(nome)
        
        self.__membros.remove(membro)
        return True
    
    def editar_membro(self, nome_atual, novo_nome=None, novo_tipo=None):
        """Edita dados de um membro"""
        membro = self.buscar_membro(nome_atual)
        if not membro:
            raise MembroNaoEncontradoException(nome_atual)
        
        if novo_nome and novo_nome.strip() and novo_nome != nome_atual:
            if self.buscar_membro(novo_nome):
                raise MembroJaExistenteException(novo_nome)
            membro._Membro__nome = novo_nome.strip()
        
        if novo_tipo and novo_tipo in Membro.TIPOS:
            membro._Membro__tipo = novo_tipo
        
        return membro
    
    def listar_membros(self):
        return self.__membros
    
    def buscar_membro(self, nome):
        for membro in self.__membros:
            if membro.nome.lower() == nome.lower():
                return membro
        return None
    
    def autenticar(self, nome, senha):
        membro = self.buscar_membro(nome)
        if not membro:
            raise MembroNaoEncontradoException(nome)
        
        if not membro.verificar_senha(senha):
            raise SenhaIncorretaException()
        
        return membro
    
    def alterar_senha_membro(self, nome, senha_atual, nova_senha):
        membro = self.buscar_membro(nome)
        if not membro:
            raise MembroNaoEncontradoException(nome)
        
        if not membro.alterar_senha(senha_atual, nova_senha):
            raise SenhaIncorretaException()
        
        return True
    
    def listar_por_tipo(self, tipo):
        return [m for m in self.__membros if m.tipo == tipo]
    
    def carregar_membros(self, membros_list):
        """Carrega lista de membros (usado pela persistência)"""
        self.__membros = membros_list