from .oscar_exception import OscarException

class ArquivoException(OscarException):
    def __init__(self, operacao, arquivo, erro_original=None):
        self.operacao = operacao
        self.arquivo = arquivo
        self.erro_original = erro_original
        message = f"Erro ao {operacao} arquivo '{arquivo}'"
        if erro_original:
            message += f": {str(erro_original)}"
        super().__init__(message)