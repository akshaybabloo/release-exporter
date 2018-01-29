import os
import unittest

import pytest

from release_exporter.exceptions import FileExists, InvalidToken
from release_exporter.requests import GitHubRequest


# ---------------------------------- GitHub -----------------------------------------


def test_GitHubRequest_fail():
    with pytest.raises(FileExists,
                       message='CHANGELOG.md already exists at ' + os.getcwd() + '. Use --force to override.'):
        a = GitHubRequest()


def test_GitHubRequest_fail_2():
    with pytest.raises(InvalidToken,
                       message="Oops! GitHub requires you to generate a private token to get the details. See "
                               "https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/ "
                               "for more information."):
        a = GitHubRequest(force=True)


class TestGitHubRequestInit(unittest.TestCase):

    def setUp(self):
        self.github_request_class = GitHubRequest(force=True, token='hello')

    def test_init(self):
        self.assertEqual(self.github_request_class.request_header, None)
        self.assertEqual(self.github_request_class.api_url, 'https://api.github.com/graphql')
        self.assertEqual(str(type(self.github_request_class.info)), "<class 'giturlparse.parser.Parsed'>")

    def test_init_condition(self):
        local_car = GitHubRequest(force=True, token='hello', repo_url='https://github.com/akshaybabloo/release-exporter')
        self.assertEqual(local_car.info.name, 'release-exporter')


# ---------------------------------- GitLab -----------------------------------------

