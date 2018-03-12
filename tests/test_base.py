import os
import unittest
from collections import namedtuple

import pytest

from release_exporter.base import FormatBase, FILE_TYPE
from release_exporter.exceptions import FileExists


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

    def test_write(self):
        with pytest.raises(NotImplementedError):
            self.format_base.write()

    def test_header(self):
        actual = """\
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

"""
        self.assertEqual(self.format_base._header(), actual)

    def test_header_rst(self):
        actual = """\
Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <http://keepachangelog.com/en/1.0.0/>`__
and this project adheres to `Semantic Versioning <http://semver.org/spec/v2.0.0.html>`__.

Unreleased_
-----------

"""
        self.assertEqual(self.format_base._header_rst(), actual)

    def test_converter(self):
        self.assertIsNone(self.format_base._converter())

    def test_total_number_releases(self):
        self.assertIs(self.format_base._total_number_releases(), None)

    def test_releases(self):
        self.assertIs(self.format_base.releases(), None)


class FormatRequestBaseBody(unittest.TestCase):
    def setUp(self):
        self.format_base = FormatBase(force=True)
        self.format_base.iter_count = 0
        self.format_base.total_number_tags = 2
        self.format_base.tag_name = 'test'
        self.format_base.date = '2008-10-10'
        self.format_base.description = 'hello'

    def test_body_less_condition(self):
        expected = '\n'.join(['## [test] - 2008-10-10',
                              '',
                              'hello'])

        self.assertIsInstance(self.format_base._body(), str)

    def test_body_else_condition(self):
        self.format_base.iter_count = 30

        expected = '\n'.join(['## test - 2008-10-10',
                              '',
                              'hello',
                              ''])
        self.assertIsInstance(self.format_base._body(), str)

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

    def test_dict_repo_template(self):
        local_nt = namedtuple('local_nt', 'name resource owner')
        k = local_nt(name='akshay', resource='some', owner='akshay')
        self.format_base.info = k
        self.format_base.total_number_tags = 10
        self.format_base.list_descriptions = []

        expected = {
            'name': "akshay",
            'resource': 'some resource',
            'owner': 'akshay',
            'repoUrl': 'https://some/akshay/akshay',
            'totalTags': 1,
            "data": []
        }

        self.assertNotEqual(self.format_base._dict_repo_template(), expected)

    def test_footer_rst(self):
        self.format_base.tag_name = '1'
        self.format_base.repo_url = "http://"

        expected = '.. _1: http://\n'
        self.assertEqual(self.format_base._footer_rst(), expected)

    def test_body_rst_less_condition(self):
        expected = '\n'.join(['test_ - 2008-10-10',
                              '',
                              'hello'])

        self.assertIsInstance(self.format_base._body_rst(), str)

    def test_body_rst_else_condition(self):
        self.format_base.iter_count = 30

        expected = '\n'.join(['test_ - 2008-10-10',
                              '',
                              'hello',
                              ''])
        self.assertIsInstance(self.format_base._body_rst(), str)


def test_file_type_constant():
    actual = {
        'markdown': '.md',
        'json': '.json',
        'rest': '.rst'
    }
    assert FILE_TYPE == actual


def test_format_base_fail():
    with pytest.raises(FileExists):
        format_base = FormatBase()


def test_format_base_file_type_fail():
    format_base = FormatBase(force=True, file_type='hello')
    assert format_base._get_file_ext() is None
