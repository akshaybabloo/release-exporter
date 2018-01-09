import os
import configparser
from giturlparse import parse
from .exceptions import ParserError
import datetime
from itertools import tee

Note = """
    ----------------------
            Details
    ----------------------
    Provider: {1}
    Repository Name: {2}
    Tags: {3}

    """


def check_provider():
    pass


def get_repo_url_info(location=os.getcwd(), url=None):
    if url is None:
        config = configparser.ConfigParser()
        config.read(location + os.sep + '.git' + os.sep + 'config')
        if 'remote "origin"' in config.sections():
            return parse(config['remote "origin"']['url'])
        else:
            raise ParserError('Git config file does not exist please provide the repository url by using --url.')
    else:
        return parse(url + '.git')


def date_convert(date):

    date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%Sz')
    date = date.strftime('%Y-%m-%d')
    return date


def pairwise(iterable):
    """Iterate in pairs

    >>> list(pairwise([0, 1, 2, 3]))
    [(0, 1), (1, 2), (2, 3)]
    >>> tuple(pairwise([])) == tuple(pairwise('x')) == ()
    True
    """
    a, b = tee(iterable)
    next(b, 'master')
    return zip(a, b)
