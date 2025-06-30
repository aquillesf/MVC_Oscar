from .oscar_exception import OscarException

class MembroJaExistenteException(OscarException):
    def __init__(self, nome):
        self.nome = nome
        message = f"Já existe um membro com o nome '{nome}'"
        super().__init__(message)