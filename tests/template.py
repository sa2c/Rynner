import unittest
import os
from unittest.mock import patch, MagicMock
from template import *


class TestTemplate(unittest.TestCase):
    def current_file(self):
        return os.path.realpath(__file__)

    def current_file_content(self):
        return open(self.current_file()).read()

    def test_instance(self):
        template = Template('template/path')

    def test_call_file(self):
        template = Template.from_file(self.current_file())

    def test_call_file(self):
        with self.assertRaises(Exception):
            template = Template.from_file('/my/test/file/poaij4oivnr')

    def test_from_file_stores_template_string(self):
        template = Template.from_file(self.current_file())
        assert template.template_string == self.current_file_content()

    def test_from_file_return_template(self):
        template = Template.from_file(self.current_file())
        assert isinstance(template, Template)

    def test_from_file_stores_template_string(self):
        template = Template('string')
        assert template.template_string == 'string'

    @patch('template.renderer')
    def test_from_file_passes_file_content_into_moustache(self, mock):
        args = MagicMock()
        file_path = MagicMock()
        self.template = Template(file_path)
        self.template.render(args)

        mock.render.assert_called_once_with(file_path, args)
