from .oscar_exception import OscarException

class PermissaoNegadaException(OscarException):
    def __init__(self, acao):
        self.acao = acao
        message = f"Permissão negada para a ação: {acao}"
        super().__init__(message)