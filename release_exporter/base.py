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

    def __init__(self, token=None, request_header=None, api_url=None, info=None, repo_url=None, *args, **kwargs):
        self.token = token
        self.request_header = request_header
        self.api_url = api_url
        self.info = info
        self.repo_url = repo_url

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
        self.all_content = []

        self.tag_name = None
        self.date = None
        self.description = None
        self.compare = None
        self.total_number_tags = None
        self.iter_count = None

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
        raise NotImplementedError('Coming soon.')

    def write_json(self):
        raise NotImplementedError('Coming soon.')

    def write_yaml(self):
        raise NotImplementedError('Coming soon.')

    @classmethod
    def _header(cls):
        return """\
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).
"""

    def _body(self):

        if self.iter_count < self.total_number_tags - 1:

            return """\
    
## [{tag_name}] - {date}

{description}
""".format(tag_name=self.tag_name, date=self.date, description=self.description)
        else:
            return """\

## {tag_name} - {date}

{description}
""".format(tag_name=self.tag_name, date=self.date, description=self.description)

    def _footer(self):
        return """\
[{tag_name}]: {url}
""".format(tag_name=self.tag_name, url=self.repo_url)

    def _converter(self):
        pass

    @classmethod
    def _dict_template(cls, tag_name=None, repo_name=None, description=None, created_at=None, compare_url=None, provider=None):

        data = {
            "tagName": tag_name,
            "repositoryName": repo_name,
            "description": description,
            "createdAt": created_at,
            "compareUrl": compare_url,
            "provider": provider
        }

        return data
