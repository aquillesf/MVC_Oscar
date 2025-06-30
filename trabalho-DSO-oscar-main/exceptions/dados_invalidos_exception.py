from .oscar_exception import OscarException

class DadosInvalidosException(OscarException):
    def __init__(self, campo, valor=None):
        self.campo = campo
        self.valor = valor
        if valor:
            message = f"Dados inválidos para o campo '{campo}': {valor}"
        else:
            message = f"Dados inválidos para o campo '{campo}'"
        super().__init__(message)