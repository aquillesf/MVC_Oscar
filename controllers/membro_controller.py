from models.membro import Membro
class MembroController:
    def __init__(self):
        self.__membros = []
    
    def criar_membro(self, nome, tipo):
        try:
            membro = Membro(nome, tipo)
            self.__membros.append(membro)
            return membro
        except ValueError:
            return None
    
    def listar_membros(self):
        return self.__membros
    
    def buscar_membro(self, nome):
        for membro in self.__membros:
            if membro.nome.lower() == nome.lower():
                return membro
        return None
    
    def login(self, nome):
        return self.buscar_membro(nome)
    
    def listar_por_tipo(self, tipo):
        return [m for m in self.__membros if m.tipo == tipo]