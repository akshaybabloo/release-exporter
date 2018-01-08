import os
import pathlib

from .exceptions import FileExists

FILE_TYPE = {
    'markdown': '.md',
    'json': '.json',
    'yaml': '.yaml'
}


class FormatBase:
    """
    Base formatter for logs.
    """

    def __init__(self, location=os.getcwd(), file_name='CHANGELOG', force=False, file_type='markdown'):

        self.location = location
        self.file_name = file_name
        self.force = force
        self.file_type = file_type

        print(location + os.sep + file_name + self._get_file_type())

        if not force:
            if pathlib.Path(location + os.sep + file_name + self._get_file_type()).is_file():
                raise FileExists(
                    file_name + self._get_file_type() + ' already exists at ' + location + '. Use --force to override.')

    def _get_file_type(self):
        try:
            return FILE_TYPE[self.file_type]
        except KeyError as e:
            print(e)

    def write_markdown(self):
        pass

    def write_json(self):
        pass

    def write_yaml(self):
        pass
