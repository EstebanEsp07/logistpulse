class DomainError(Exception):
    """Error de regla de negocio con código HTTP asociado."""

    def __init__(self, message, status=400):
        super().__init__(message)
        self.message = message
        self.status = status
