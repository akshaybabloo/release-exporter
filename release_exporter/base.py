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

    def __init__(self, token=None, request_header=None, api_url=None, info=None, url=None, *args, **kwargs):
        self.token = token
        self.request_header = request_header
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
        self.tag = None
        self.date = None
        self.content = None
        self.compare = None

        self.location = location
        self.file_name = file_name
        self.force = force
        self.file_type = file_type
        self.all_content = []

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

    @classmethod
    def _header(cls):
        return """\
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).
"""

    def _body(self):
        return """\

## [{tag}] - {date}

{content}
""".format(tag=self.tag, date=self.date, content=self.content)

    def _footer(self):
        return """\
[{tag}]: {url}
""".format(tag=self.tag, url=self.url)

    def _converter(self):
        pass
