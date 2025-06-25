class OscarException(Exception):
    def __init__(self, message="Erro no sistema Oscar"):
        self.message = message
        super().__init__(self.message)