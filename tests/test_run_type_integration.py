import unittest
from unittest.mock import MagicMock as MM
from rynner.run_type import RunType, RunAction
from rynner.inputs import Interface, TextInput, RunnerConfigDialog
from tests.qtest_helpers import QTestCase
from PySide2.QtTest import QTest


class TestRunTypeIntegration(QTestCase):
    def setUp(self):
        self.interface = Interface([
            TextInput('key', 'My Label', default="My Default"),
            TextInput(
                'another_key', 'My Other Label', default="My Other Default"),
        ])
        self.runner = lambda data: None

    def create_run_type(self):
        self.run_type = RunType(self.runner, self.interface)

    def test_configure_and_run_empty_runner(self):
        self.create_run_type()

        self.assertNotQVisible(self.run_type.interface.dialog)

        self.run_type.create()

        self.assertQVisible(self.run_type.interface.dialog)

    @unittest.skip('expected failure')
    def test_dialog_window_test_behaviour(self):
        # - window title
        # - validation
        # - reset values
        # - multiple initialisations same widget
        # - converting to values
        assert False
