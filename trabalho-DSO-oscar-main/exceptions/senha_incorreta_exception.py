from .oscar_exception import OscarException

class SenhaIncorretaException(OscarException):
    def __init__(self):
        message = "Senha incorreta"
        super().__init__(message)