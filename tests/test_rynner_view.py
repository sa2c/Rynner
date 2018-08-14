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

    def test_has_adds_widgets_as_child(self):

        input = TextInput('key', 'label')

        assert QLineEdit not in input.children()
        assert QLabel not in input.children()

    def test_sets_default_text_in_text_edit(self):
        input = TextInput('key', 'label', default='default string')
        self.assertEqual(input.value(), 'default string')

    def test_result_contains_children(self):
        input = TextInput('key', 'label')

        types = [type(child) for child in input.children()]
        self.assertIn(QLineEdit, types)
        self.assertIn(QLabel, types)

    def test_label_contains_text(self):
        input = TextInput('key', 'My label')
        qlabel_text = next(child.text() for child in input.children()
                           if type(child) == QLabel)

        self.assertEqual(qlabel_text, "My label")

    def test_input_added_to_layout(self):
        input = TextInput('key', 'My label')
        self.assertEqual(input.layout().itemAt(1).widget(), input.input)

    def test_label_added_to_layout(self):
        input = TextInput('key', 'My label')

        self.assertEqual(input.layout().itemAt(0).widget(), input.label)

    def test_reset_leaves_value_by_default(self):
        input = TextInput('key', 'My label')
        input.show()

        QTest.keyClicks(input.input, "My Input Text")

        self.assertEqual(input.input.text(), "My Input Text")

        input.reset()

        self.assertEqual(input.input.text(), "My Input Text")

    def test_resets_uses_default_as_initial(self):
        input = TextInput('key', 'My label', default="default value")

        input.show()

        self.assertEqual(input.input.text(), "default value")

    def test_resets_if_reset_true(self):
        input = TextInput(
            'key', 'My label', default="default value", reset=True)

        input.show()

        QTest.keyClicks(input.input, " and some more text")

        self.assertEqual(input.input.text(), "My Input Text")

        input.reset()

        self.assertEqual(input.input.text(), "default value")
