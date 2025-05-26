from models.membro import Membro

class MembroController:
    def __init__(self):
        self.__membros = []
    
    def criar_membro(self, nome, tipo, senha):
        if self.buscar_membro(nome):
            raise ValueError("Já existe um membro com este nome")
        
        try:
            membro = Membro(nome, tipo, senha)
            self.__membros.append(membro)
            return membro
        except ValueError as e:
            raise e
    
    def listar_membros(self):
        return self.__membros
    
    def buscar_membro(self, nome):
        for membro in self.__membros:
            if membro.nome.lower() == nome.lower():
                return membro
        return None
    
    def autenticar(self, nome, senha):
        membro = self.buscar_membro(nome)
        if membro and membro.verificar_senha(senha):
            return membro
        return None
    
    def alterar_senha_membro(self, nome, senha_atual, nova_senha):
        membro = self.buscar_membro(nome)
        if membro:
            return membro.alterar_senha(senha_atual, nova_senha)
        return False
    
    def listar_por_tipo(self, tipo):
        return [m for m in self.__membros if m.tipo == tipo]