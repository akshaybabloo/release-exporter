class FileExists(Exception):
    """
    This exception is raised when a file exists..
    """

    def __init__(self, message, errors=None):
        super(FileExists, self).__init__(message)

        self.errors = errors
