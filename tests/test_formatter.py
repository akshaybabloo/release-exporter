import io
import os
import unittest
from unittest.mock import patch

from release_exporter.formatter import github, gitlab


# ------------------------- GitHub --------------------------


class TestGitHubFormatMarkdown(unittest.TestCase):

    def setUp(self):
        self.github_format = github(force=True, token=os.environ['GITHUB_TOKEN'],
                                    repo_url='https://github.com/akshaybabloo/release-exporter')

    @patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout_1(self, n, expected_output, mock_stdout):
        request = self.github_format._converter()
        self.assertIn(expected_output, mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout_2(self, n, expected_output, mock_stdout):
        request = self.github_format.write_markdown()
        self.assertIn(expected_output, mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout_3(self, n, expected_output, mock_stdout):
        request = self.github_format.write()
        self.assertIn(expected_output, mock_stdout.getvalue())

    def test_convert(self):
        request = self.github_format._converter()

        self.assertIsInstance(request, tuple)
        self.assertIn('changelog', request[0])

    def test_output(self):
        self.assert_stdout_1('', 'Provider')

    def test_write_markdown(self):
        self.assert_stdout_2('', 'Done')

    def test_write(self):
        self.assert_stdout_3('', 'created')


class TestGitHubFormatJson(unittest.TestCase):

    def setUp(self):
        self.github_format = github(force=True, token=os.environ['GITHUB_TOKEN'],
                                    repo_url='https://github.com/akshaybabloo/release-exporter', file_type='json')

    @patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout_1(self, n, expected_output, mock_stdout):
        request = self.github_format._converter()
        self.assertIn(expected_output, mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout_2(self, n, expected_output, mock_stdout):
        request = self.github_format.write_json()
        self.assertIn(expected_output, mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout_3(self, n, expected_output, mock_stdout):
        request = self.github_format.write()
        self.assertIn(expected_output, mock_stdout.getvalue())

    def test_convert(self):
        request = self.github_format._converter()

        self.assertIs(request, None)
        self.assertIn('provider', self.github_format._dict_repo_template())

    def test_output(self):
        self.assert_stdout_1('', 'Provider')

    def test_write_markdown(self):
        self.assert_stdout_2('', 'Done')

    def test_write(self):
        self.assert_stdout_3('', 'created')


# ------------------------- GitLab --------------------------


class TestGitLabFormatMarkdown(unittest.TestCase):

    def setUp(self):
        self.gitlab_format = gitlab(force=True, token=os.environ['GITLAB_TOKEN'],
                                    repo_url='https://gitlab.com/akshaybabloo/test-releases')

    @patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout_1(self, n, expected_output, mock_stdout):
        request = self.gitlab_format._converter()
        self.assertIn(expected_output, mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout_2(self, n, expected_output, mock_stdout):
        request = self.gitlab_format.write_markdown()
        self.assertIn(expected_output, mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout_3(self, n, expected_output, mock_stdout):
        request = self.gitlab_format.write()
        self.assertIn(expected_output, mock_stdout.getvalue())

    def test_convert(self):
        request = self.gitlab_format._converter()

        self.assertIsInstance(request, tuple)
        self.assertIn('changelog', request[0])

    def test_output(self):
        self.assert_stdout_1('', 'Provider')

    def test_write_markdown(self):
        self.assert_stdout_2('', 'Done')

    def test_write(self):
        self.assert_stdout_3('', 'created')


class TestGitLabFormatJson(unittest.TestCase):

    def setUp(self):
        self.gitlab_format = gitlab(force=True, token=os.environ['GITLAB_TOKEN'],
                                    repo_url='https://gitlab.com/akshaybabloo/test-releases', file_type='json')

    @patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout_1(self, n, expected_output, mock_stdout):
        request = self.gitlab_format._converter()
        self.assertIn(expected_output, mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout_2(self, n, expected_output, mock_stdout):
        request = self.gitlab_format.write_json()
        self.assertIn(expected_output, mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout_3(self, n, expected_output, mock_stdout):
        request = self.gitlab_format.write()
        self.assertIn(expected_output, mock_stdout.getvalue())

    def test_convert(self):
        request = self.gitlab_format._converter()

        self.assertIs(request, None)
        self.assertIn('provider', self.gitlab_format._dict_repo_template())

    def test_output(self):
        self.assert_stdout_1('', 'Provider')

    def test_write_markdown(self):
        self.assert_stdout_2('', 'Done')

    def test_write(self):
        self.assert_stdout_3('', 'created')
