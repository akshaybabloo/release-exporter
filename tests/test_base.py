import os
import unittest

import pytest

from release_exporter.base import RequestBase, FormatBase, FILE_TYPE
from release_exporter.exceptions import FileExists


class TestRequestBase(unittest.TestCase):
    def setUp(self):
        self.request_base = RequestBase()

    def test_class_args(self):
        self.assertIsNone(self.request_base.token)
        self.assertIsNone(self.request_base.request_header)
        self.assertIsNone(self.request_base.api_url)
        self.assertIsNone(self.request_base.info)
        self.assertIsNone(self.request_base.repo_url)

    def test_total_number_releases(self):
        self.assertIsNone(self.request_base._total_number_releases())

    def test_releases(self):
        self.assertIsNone(self.request_base.releases())


class TestFormatBase(unittest.TestCase):

    def setUp(self):
        self.format_base = FormatBase(force=True)

    def test_args(self):
        self.assertEqual(self.format_base.location, os.getcwd())
        self.assertEqual(self.format_base.file_name, 'CHANGELOG')
        self.assertTrue(self.format_base.force)
        self.assertEqual(self.format_base.file_type, 'markdown')
        self.assertEqual(self.format_base.all_content, [])
        self.assertIsNone(self.format_base.tag_name)
        self.assertIsNone(self.format_base.date)
        self.assertIsNone(self.format_base.description)
        self.assertIsNone(self.format_base.compare_url)
        self.assertIsNone(self.format_base.total_number_tags)
        self.assertIsNone(self.format_base.iter_count)
        self.assertEqual(self.format_base.list_descriptions, [])

    def test_get_file_ext(self):
        self.assertEqual(self.format_base._get_file_ext(), '.md')

    def test_write_markdown(self):
        with pytest.raises(NotImplementedError):
            self.format_base.write_markdown()

    def test_write_json(self):
        with pytest.raises(NotImplementedError):
            self.format_base.write_json()

    def test_header(self):
        actual = """\
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

"""
        self.assertEqual(self.format_base._header(), actual)

    def test_converter(self):
        self.assertIsNone(self.format_base._converter())


class FormatRequestBaseBody(unittest.TestCase):
    def setUp(self):
        self.format_base = FormatBase(force=True)
        self.format_base.iter_count = 0
        self.format_base.total_number_tags = 2
        self.format_base.tag_name = 'test'
        self.format_base.date = '2008-10-10'
        self.format_base.description = 'hello'

    # def test_body_less_condition(self):
    #
    #     expected = '\n'.join(['## [test] - 2008-10-10',
    #                           '',
    #                           'hello'])
    #
    #     self.assertAlmostEqual(self.format_base._body(), expected)

    # def test_body_else_condition(self):
    #     self.format_base.iter_count = 30
    #
    #     expected = '\n'.join(['## test - 2008-10-10',
    #                           '',
    #                           'hello',
    #                           ''])
    #     self.assertEqual(self.format_base._body(), expected)

    def test_footer(self):
        self.format_base.tag_name = '1'
        self.format_base.repo_url = "http://"

        expected = '[1]: http://\n'
        self.assertEqual(self.format_base._footer(), expected)

    def test__dict_data_template(self):
        expected = {
            "tagName": '1',
            "description": 'hello',
            "createdAt": '2008-10-10',
            "compareUrl": 'http://'
        }

        self.assertEqual(self.format_base._dict_data_template('1', 'hello', '2008-10-10', 'http://'), expected)

    # def test_dict_repo_template(self):
    #     self.format_base.info = namedtuple('info', 'name resource owner')
    #     self.format_base.info(name='akshay', resource='some', owner='akshay')
    #     self.format_base.total_number_tags = 10
    #     self.format_base.list_descriptions = []
    #
    #
    #
    #     expected = {
    #         'name': "akshay",
    #         'resource': 'some resource',
    #         'owner': 'akshay',
    #         'repoUrl': 'https://some/akshay/akshay',
    #         'totalTags': 1,
    #         "data": []
    #     }
    #     #
    #     print(self.format_base.info.name)
    #     # print(self.format_base._dict_repo_template())
    #     # self.assertEqual(self.format_base._dict_repo_template(), expected)


def test_file_type_constant():
    actual = {
        'markdown': '.md',
        'json': '.json',
    }
    assert FILE_TYPE == actual


def test_format_base_fail():
    with pytest.raises(FileExists):
        format_base = FormatBase()


def test_format_base_file_type_fail():
    format_base = FormatBase(force=True, file_type='hello')
    assert format_base._get_file_ext() == None
