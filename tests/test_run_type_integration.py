import unittest
from unittest.mock import MagicMock as MM
from run_type import RunType, RunAction
from inputs import Interface, TextInput
from PySide2.QtWidgets import QApplication

app = QApplication()


class TestRunTypeIntegration(unittest.TestCase):
    def setUp(self):
        pass

    def test_configure_and_run_empty_runner(self):
        interface = Interface([
            TextInput('key', 'My Label', default="My Default"),
            TextInput(
                'another_key', 'My Other Label', default="My Other Default"),
        ])

        def runner(data):
            pass

        def some_action(data):
            pass

        run_type = RunType(runner, interface)

        run_type.add_action('Some Action', some_action)

        run_type.create()
