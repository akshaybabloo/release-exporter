import json
import os
import unittest
from unittest.mock import patch

import pytest

from release_exporter.exceptions import FileExists, InvalidToken
from release_exporter.request import GitHubRequest, GitLabRequest


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
        local_car = GitHubRequest(force=True, token='hello',
                                  repo_url='https://github.com/akshaybabloo/release-exporter')
        self.assertEqual(local_car.info.name, 'release-exporter')


class TestGitHubRequestFail(unittest.TestCase):

    def setUp(self):
        self.github_request_class = GitHubRequest(force=True, token='hello')

    def test_total_number_releases(self):
        with pytest.raises(KeyError, message='Wrong credentials given. Please check if you have the correct token.'):
            response = self.github_request_class._total_number_releases()

    def test_releases(self):
        with pytest.raises(KeyError, message='Wrong credentials given. Please check if you have the correct token.'):
            response = self.github_request_class.releases()


class TestGitHubRequest(unittest.TestCase):

    def setUp(self):
        self.github_request_class = GitHubRequest(force=True, token=os.environ['GITHUB_TOKEN'],
                                                  repo_url='https://github.com/akshaybabloo/release-exporter')

    def test_total_number_releases(self):
        response = self.github_request_class._total_number_releases()

        self.assertIsInstance(response, int)

    def test_release(self):
        response = self.github_request_class.releases()
        self.assertIn('tag', json.dumps(response))


# ---------------------------------- GitLab -----------------------------------------


def test_GitLabRequest_fail():
    with pytest.raises(FileExists,
                       message='CHANGELOG.md already exists at ' + os.getcwd() + '. Use --force to override.'):
        a = GitLabRequest()


def test_GitLabRequest_fail_2():
    with pytest.raises(InvalidToken,
                       message="Oops! GitLab requires you to generate a private token to get the details. See "
                               "https://docs.gitlab.com/ce/user/profile/personal_access_tokens.html "
                               "for more information."):
        a = GitLabRequest(force=True)


class TestGitLabRequestInit(unittest.TestCase):

    def setUp(self):
        self.gitlab_request_class = GitLabRequest(force=True, token='hello')

    def test_init(self):
        self.assertEqual(self.gitlab_request_class.request_header, None)
        self.assertEqual(self.gitlab_request_class.api_url, 'https://gitlab.com/api/v4/')
        self.assertEqual(str(type(self.gitlab_request_class.info)), "<class 'giturlparse.parser.Parsed'>")

    def test_init_condition(self):
        local_car = GitHubRequest(force=True, token='hello',
                                  repo_url='https://gitlab.com/akshaybabloo/test-releases')
        self.assertEqual(local_car.info.name, 'test-releases')


class TestGitLabRequestFail(unittest.TestCase):

    def setUp(self):
        self.gitlab_request_class = GitLabRequest(force=True, token='hello')

    def test_repo_id(self):
        with pytest.raises(KeyError, message='Wrong credentials given. Please check if you have the correct token.'):
            response = self.gitlab_request_class._repo_id()

    def test_releases(self):
        with pytest.raises(KeyError, message='Wrong credentials given. Please check if you have the correct token.'):
            response = self.gitlab_request_class.releases()


class TestGitLabRequest(unittest.TestCase):

    def setUp(self):
        self.gitlab_request_class = GitLabRequest(force=True, token=os.environ['GITLAB_TOKEN'],
                                                  repo_url='https://gitlab.com/akshaybabloo/test-releases')

    def test_repo_id(self):
        response = self.gitlab_request_class._repo_id()

        self.assertIsInstance(response, int)

    def test_release(self):
        response = self.gitlab_request_class.releases()
        self.assertIn('tag_name', json.dumps(response))


def test_GitLab_repo_id():
    gitlab_request_class = GitLabRequest(force=True, token=os.environ['GITLAB_TOKEN'],
                                         repo_url='https://gitlab.com/akshaybabloo/public')

    with patch('builtins.input', return_value='12345'):
        assert gitlab_request_class._repo_id() == '12345'
