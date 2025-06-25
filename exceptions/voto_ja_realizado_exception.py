from .oscar_exception import OscarException


class VotoJaRealizadoException(OscarException):
    def __init__(self, categoria):
        self.categoria = categoria
        message = f"Você já votou na categoria '{categoria}'"
        super().__init__(message)