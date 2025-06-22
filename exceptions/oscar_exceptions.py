class OscarException(Exception):
    def __init__(self, message="Erro no sistema Oscar"):
        self.message = message
        super().__init__(self.message)

class MembroJaExistenteException(OscarException):
    def __init__(self, nome):
        self.nome = nome
        message = f"Já existe um membro com o nome '{nome}'"
        super().__init__(message)

class MembroNaoEncontradoException(OscarException):
    def __init__(self, nome):
        self.nome = nome
        message = f"Membro '{nome}' não encontrado"
        super().__init__(message)

class SenhaIncorretaException(OscarException):
    def __init__(self):
        message = "Senha incorreta"
        super().__init__(message)

class PermissaoNegadaException(OscarException):
    def __init__(self, acao):
        self.acao = acao
        message = f"Permissão negada para a ação: {acao}"
        super().__init__(message)

class ItemNaoEncontradoException(OscarException):
    def __init__(self, tipo_item, identificador):
        self.tipo_item = tipo_item
        self.identificador = identificador
        message = f"{tipo_item} '{identificador}' não encontrado"
        super().__init__(message)

class VotoJaRealizadoException(OscarException):
    def __init__(self, categoria):
        self.categoria = categoria
        message = f"Você já votou na categoria '{categoria}'"
        super().__init__(message)

class DadosInvalidosException(OscarException):
    def __init__(self, campo, valor=None):
        self.campo = campo
        self.valor = valor
        if valor:
            message = f"Dados inválidos para o campo '{campo}': {valor}"
        else:
            message = f"Dados inválidos para o campo '{campo}'"
        super().__init__(message)

class ArquivoException(OscarException):
    def __init__(self, operacao, arquivo, erro_original=None):
        self.operacao = operacao
        self.arquivo = arquivo
        self.erro_original = erro_original
        message = f"Erro ao {operacao} arquivo '{arquivo}'"
        if erro_original:
            message += f": {str(erro_original)}"
        super().__init__(message)