import os
import pathlib

from .exceptions import FileExists

FILE_TYPE = {
    'markdown': '.md',
    'json': '.json',
    'yaml': '.yaml'
}


class RequestBase:
    """
    Base class for requests.
    """

    def __init__(self, token=None, header=None, api_url=None, info=None, url=None, *args, **kwargs):
        self.token = token
        self.header = header
        self.api_url = api_url
        self.info = info
        self.url = url

    def _total_number_releases(self):
        pass

    def releases(self):
        pass


class FormatBase(RequestBase):
    """
    Base formatter for logs.
    """

    def __init__(self, location=os.getcwd(), file_name='CHANGELOG', force=False, file_type='markdown', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.location = location
        self.file_name = file_name
        self.force = force
        self.file_type = file_type

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

    def process(self):
        pass
