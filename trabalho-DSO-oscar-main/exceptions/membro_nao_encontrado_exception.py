from .oscar_exception import OscarException

class MembroNaoEncontradoException(OscarException):
    def __init__(self, nome):
        self.nome = nome
        message = f"Membro '{nome}' não encontrado"
        super().__init__(message)