class FileExists(Exception):
    """
    This exception is raised when a file exists.
    """

    def __init__(self, message, errors=None):
        super(FileExists, self).__init__(message)

        self.errors = errors


class ParserError(Exception):
    """
    This exception is raised Git config file does not exist.
    """

    def __init__(self, message, errors=None):
        super(ParserError, self).__init__(message)

        self.errors = errors


class UnknownRepo(Exception):
    """
    This exception is raised Git config file does not exist.
    """

    def __init__(self, message, errors=None):
        super(UnknownRepo, self).__init__(message)

        self.errors = errors
