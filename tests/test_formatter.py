import io
import os
import unittest
from unittest.mock import patch

from release_exporter.formatter import github


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

    def test_convert(self):
        request = self.github_format._converter()

        self.assertIsInstance(request, tuple)
        self.assertIn('changelog', request[0])

    def test_output(self):
        self.assert_stdout_1('', 'Provider')

    def test_write_markdown(self):
        self.assert_stdout_2('', 'Done')


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

    def test_convert(self):
        request = self.github_format._converter()

        self.assertIs(request, None)
        self.assertIn('provider', self.github_format._dict_repo_template())

    def test_output(self):
        self.assert_stdout_1('', 'Provider')

    def test_write_markdown(self):
        self.assert_stdout_2('', 'Done')
