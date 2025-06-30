from .oscar_exception import OscarException

class ItemNaoEncontradoException(OscarException):
    def __init__(self, tipo_item, identificador):
        self.tipo_item = tipo_item
        self.identificador = identificador
        message = f"{tipo_item} '{identificador}' não encontrado"
        super().__init__(message)