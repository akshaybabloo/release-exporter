import os
import pathlib

from .exceptions import FileExists

FILE_TYPE = {
    'markdown': '.md',
    'json': '.json',
    'rest': '.rst'
}


class FormatBase:
    """
    Base formatter for logs.
    """

    def __init__(self, token=None, request_header=None, api_url=None, info=None, repo_url=None, location=os.getcwd(),
                 file_name='CHANGELOG', force=False, file_type='markdown'):

        self.location = location
        self.file_name = file_name
        self.force = force
        self.file_type = file_type
        self.all_content = []
        self.token = token
        self.request_header = request_header
        self.api_url = api_url
        self.info = info
        self.repo_url = repo_url

        self.tag_name = None
        self.date = None
        self.description = None
        self.compare_url = None
        self.total_number_tags = None
        self.iter_count = None
        self.list_descriptions = []

        if not force:
            if pathlib.Path(location + os.sep + file_name + self._get_file_ext()).is_file():
                raise FileExists(f"{file_name} {self._get_file_ext()} already exists at {location}. Use --force to override or force=True.'")

    def _get_file_ext(self):
        try:
            return FILE_TYPE[self.file_type]
        except KeyError as e:
            print(e)

    def write(self):
        raise NotImplementedError('Coming soon.')

    @classmethod
    def _header(cls):
        return """\
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

"""

    def _body(self):

        if self.iter_count < self.total_number_tags - 1:

            return f"""\
    
## [{self.tag_name}] - {self.date}

{self.description}
"""
        else:
            return f"""\

## {self.tag_name} - {self.date}

{self.description}

"""

    def _footer(self):
        return """\
[{tag_name}]: {url}
""".format(tag_name=self.tag_name, url=self.repo_url)

    def _converter(self):
        pass

    def _dict_repo_template(self):

        repo = {
            "repositoryName": self.info.name,
            "provider": self.info.resource,
            "owner": self.info.owner,
            "repoUrl": 'https://' + self.info.resource + '/' + self.info.owner + '/' + self.info.name,
            "totalTags": self.total_number_tags,
            "data": self.list_descriptions
        }

        return repo

    @classmethod
    def _dict_data_template(cls, tag_name=None, description=None, date=None, compare_url=None):

        data = {
            "tagName": tag_name,
            "description": description,
            "createdAt": date,
            "compareUrl": compare_url
        }

        return data

    def _total_number_releases(self):
        pass

    def releases(self):
        pass

    @classmethod
    def _header_rst(cls):
        return """\
Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <http://keepachangelog.com/en/1.0.0/>`__
and this project adheres to `Semantic Versioning <http://semver.org/spec/v2.0.0.html>`__.

Unreleased_
-----------

"""

    def _body_rst(self):

        if self.iter_count < self.total_number_tags - 1:

            return f"""\

{self.tag_name}_ - {self.date}
~~~~~~~~~~~~~~~~~~~~~~~~~~

{self.description}
"""
        else:
            return f"""\

{self.tag_name} - {self.date}
~~~~~~~~~~~~~~~~~~~~~~~~~~

{self.description}

"""

    def _footer_rst(self):
        return f"""\
.. _{self.tag_name}: {self.repo_url}
"""
