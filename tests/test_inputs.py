import unittest
from unittest.mock import MagicMock as MM
from unittest.mock import patch
from PySide2.QtTest import QTest
import rynner
from rynner.inputs import *
from tests.qtest_helpers import QTestCase


class TestTextInput(unittest.TestCase):
    def setUp(self):
        pass

    def instance(self, **kwargs):
        self.input = TextInput('key', 'Label', **kwargs)

    def type_text(self, text):
        QTest.keyClicks(self.input.widget, text)

    def test_instance(self):
        self.instance()

    def test_can_type_text(self):
        self.instance()
        self.type_text("some input")

    def test_value_method_return_text(self):
        self.instance()
        self.type_text("some input")
        self.assertEqual(self.input.value(), "some input")

    def test_show_qwidget(self):
        input = TextInput('key', 'label')
        input.init()

    def test_has_adds_widgets_as_child(self):
        input = TextInput('key', 'label')

        self.assertIsInstance(input.widget, QLineEdit)

    def test_sets_default_text_in_text_edit(self):
        input = TextInput('key', 'label', default='default string')
        self.assertEqual(input.value(), 'default string')

    def test_label_contains_text(self):
        input = TextInput('key', 'My label')

        self.assertEqual(input.label.text(), "My label")
        self.assertIsInstance(input.label, QLabel)

    @unittest.skip('refactor breaks: Interface should handle labels now')
    def test_label_added_to_layout(self):
        pass

    def test_reset_leaves_value_by_default(self):
        input = TextInput('key', 'My label')
        input.init()

        QTest.keyClicks(input.widget, "My Input Text")

        self.assertEqual(input.value(), "My Input Text")

        input.init()

        self.assertEqual(input.value(), "My Input Text")

    def test_uses_default_as_initial(self):
        input = TextInput('key', 'My label', default="default value")

        input.init()

        self.assertEqual(input.value(), "default value")

    def test_no_reset_as_default(self):
        input = TextInput('key', 'My label', default="default value")

        QTest.keyClicks(input.widget, " and some more text")

        value = input.value()
        self.assertNotEqual(input.value(), "default value")

        input.init()

        # input value remains the same on calls to init
        self.assertEqual(input.value(), value)

    def test_resets_if_reset_true(self):
        input = TextInput(
            'key', 'My label', default="default value", remember=False)

        QTest.keyClicks(input.widget, " and some more text")

        self.assertNotEqual(input.value(), "default value")

        input.init()

        self.assertEqual(input.value(), "default value")

    def test_stores_key(self):
        mock_key = MM()
        input = TextInput(mock_key, 'label')

        self.assertEqual(input.key, mock_key)

    def test_cli_asks_for_input(self):
        input = TextInput('key', 'Test Label')

        input_data = "Test Input Data"

        with patch.object(
                rynner.inputs, "input", create=True, return_value=input_data):
            value = input.cli()
            self.assertEqual(value, input_data)

    @patch('rynner.inputs.input')
    def test_cli_correct_label(self, mock_input):
        input = TextInput('key', 'Test Label')

        value = input.cli()
        mock_input.assert_called_once_with('Test Label')

    def test_default_TextInput_is_valid(self):
        self.instance()
        self.assertTrue(self.input.valid())


class InterfaceTestInput(QTestCase):
    def setUp(self):
        self.children = [
            TextInput('key1', 'My label 1'),
            TextInput('key2', 'My label 2'),
            TextInput('key3', 'My label 3')
        ]

    def children_widgets(self):
        return [child.widget for child in self.children]

    def instance(self):
        self.interface = Interface(self.children)

    def interface_widget(self):
        return self.interface.dialog.layout().itemAt(0).widget()

    def test_instance(self):
        self.instance()

    def test_create_dialog(self):
        self.instance()
        self.assertIsInstance(self.interface.dialog, QDialog)

    def test_widgets_added_as_children_of_dialog(self):
        self.instance()

        widget_children = self.interface_widget().children()
        for child in self.children:
            self.assertIn(child.widget, widget_children)

    def test_all_keys_must_be_unique(self):

        first = self.children[0]

        self.children.append(TextInput(first.key, first.label))

        with self.assertRaises(DuplicateKeyException) as context:
            self.instance()

        self.assertIn(first.key, str(context.exception))

    def test_widgets_added_to_layout(self):
        self.instance()

        for index, child in enumerate(self.children):
            interface_widget = self.interface_widget()
            in_layout = interface_widget.layout().itemAt(index).widget()
            in_field = child.widget

            self.assertEqual(in_layout, in_field)

    def test_data_returns_data_from_children(self):
        self.children = [
            TextInput('key1', 'Label', default='default1'),
            TextInput('key2', 'Label', default='default2')
        ]
        self.instance()
        self.assertEqual(self.interface.data(), {
            'key1': 'default1',
            'key2': 'default2'
        })

    def test_valid_returns_empty_if_no_invalid_children(self):
        self.instance()
        invalid = self.interface.invalid()
        self.assertEqual(len(invalid), 0)

    def test_valid_true_if_children_valid(self):

        self.children[0].valid = lambda: False

        self.instance()

        self.assertEqual(self.interface.invalid(), [self.children[0]])

    def test_creates_and_shows_dialog(self):
        self.instance()
        self.assertNotQVisible(self.children_widgets())
        self.interface.show()
        self.assertQVisible(self.children_widgets())

        assert self.interface.dialog.isVisible()
        for child in self.children:
            assert child.widget.isVisible()

    @patch('rynner.inputs.RunnerConfigDialog')
    def test_show_returns_the_output_of_dialog_show(self, MockConfigDialog):
        self.instance()
        accepted = self.interface.show()
        dialog_exec_return = MockConfigDialog().open()
        self.assertEqual(accepted, dialog_exec_return)

    def test_resets_children(self):
        input1 = TextInput("key1", "label", default="default", remember=False)
        input2 = TextInput("key2", "label", default="default", remember=True)

        self.children = [input1, input2]
        self.instance()

        # type into inputs
        for child in self.children:
            QTest.keyClicks(child.widget, " some text")

        self.interface.show()

        values = self.interface.data()

        self.assertEqual(values, {
            'key1': 'default',
            'key2': 'default some text'
        })


class TestRunnerConfigDialogClass(unittest.TestCase):
    def setUp(self):
        self.dialog_title = "Title"
        self.widget = QWidget()

    def instance(self):
        self.dialog = RunnerConfigDialog(self.dialog_title, self.widget)

    def instance_items(self):
        layout = self.dialog.layout()
        return [layout.itemAt(i).widget() for i in range(layout.count())]

    def test_instance(self):
        self.instance()

    def test_title(self):
        self.instance()
        self.assertEqual(self.dialog.windowTitle(), self.dialog_title)

    def test_widget_in_layout(self):
        self.instance()
        items = self.instance_items()

        self.assertIn(self.widget, items)

    def test_buttons_in_layout(self):
        self.instance()
        type_items = list(map(type, self.instance_items()))

        self.assertIn(QDialogButtonBox, type_items)

    def test_instantiate_twice_same_widget(self):
        self.instance()
        self.assertEqual(self.widget.parent(), self.dialog)
        self.instance()
        self.assertEqual(self.widget.parent(), self.dialog)

    def test_shows_dialog_with_title(self):
        input = TextInput("key", "label")
        dialog = RunnerConfigDialog("MY WINDOW TITLE", input.widget)
        self.assertFalse(input.widget.isVisible())
        dialog.show()
        self.assertTrue(input.widget.isVisible())
        self.assertEqual(dialog.windowTitle(), "MY WINDOW TITLE")

    def test_shows_dialog_twice(self):
        input = TextInput("key", "label")
        dialog = RunnerConfigDialog("MY WINDOW TITLE", input.widget)

        # Show once
        self.assertFalse(input.widget.isVisible())
        dialog.show()
        self.assertTrue(input.widget.isVisible())
        dialog.close()
        self.assertFalse(input.widget.isVisible())

        # Show again
        self.assertFalse(input.widget.isVisible())
        dialog.show()
        self.assertTrue(input.widget.isVisible())
        dialog.close()
        self.assertFalse(input.widget.isVisible())
