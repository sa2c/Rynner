import unittest
from unittest.mock import MagicMock as MM
from unittest.mock import patch
from PySide2.QtTest import QTest
from rynner_view import *

app = QApplication(sys.argv)


class TestTextInput(unittest.TestCase):
    def setUp(self):
        pass

    def instance(self, **kwargs):
        self.input = TextInput('key', 'Label', **kwargs)

    def type_text(self, text):
        QTest.keyClicks(self.input.input, text)

    def test_instance(self):
        self.instance()

    def test_can_type_text(self):
        self.instance()
        self.type_text("some input")

    def test_value_method_return_text(self):
        self.instance()
        self.type_text("some input")
        self.assertEqual(self.input.value(), "some input")

    def test_validate_returns_true_by_default(self):
        self.instance()
        self.type_text("some input")
        self.assertTrue(self.input.valid())

    def test_validate_return_value(self):
        mock_text = "some input"
        validation = lambda input: input == mock_text
        self.instance(validation=validation)
        self.type_text("some input")
        self.assertTrue(self.input.valid())
        self.type_text("some input")
        self.assertFalse(self.input.valid())

    def test_validate_validation_is_called(self):
        validation = MM()
        self.instance(validation=validation)
        self.type_text("some input")
        self.input.valid()
        validation.assert_called_once_with("some input")

    def test_input_knows_its_key(self):
        key = MM()
        input = TextInput(key, 'label')
        self.assertEqual(input.key, key)

    def test_show_qwidget(self):
        input = TextInput('key', 'label')
        input.show()

    def test_show_call_init_with_parent(self):
        mock_parent = QWidget()

        input = TextInput('key', 'label', parent=mock_parent)
        self.assertEqual(input.parent(), mock_parent)

    def test_show_call_init_with_none_by_default(self):
        mock_parent = None

        input = TextInput('key', 'label', parent=mock_parent)
        self.assertEqual(input.parent(), mock_parent)

    def test_sets_layout(self):
        input = TextInput('key', 'label')
        self.assertIsInstance(input.layout(), QVBoxLayout)

    def test_has_addWidget_method(self):

        input = TextInput('key', 'label')
        mock_widget = QWidget()

        assert mock_widget not in input.children()

        input.addWidget(mock_widget)

        assert mock_widget in input.children()

    def test_sets_default_text_in_text_edit(self):
        input = TextInput('key', 'label', default='default string')
        self.assertEqual(input.value(), 'default string')

    def my_test_QTextEdit_is_child(self):
        pass
