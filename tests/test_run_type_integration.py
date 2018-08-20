import unittest
from PySide2.QtCore import QTimer
from unittest.mock import MagicMock as MM
from rynner.run_type import RunType, RunAction
from rynner.inputs import Interface, TextInput, RunnerConfigDialog
from tests import qtest_helpers
from PySide2.QtTest import QTest


class TestRunTypeIntegration(qtest_helpers.QTestCase):
    def setUp(self):
        self.interface = Interface([
            TextInput('key', 'My Label', default="My Default"),
            TextInput(
                'another_key', 'My Other Label', default="My Other Default"),
        ])
        self.runner = lambda data: None

    def instance_run_type(self):
        self.run_type = RunType(self.runner, self.interface)
        button_box = self.run_type.interface.dialog._button_box
        self.ok_button = qtest_helpers.get_button(button_box, 'ok')
        self.cancel_button = qtest_helpers.get_button(button_box, 'cancel')

    def test_show_config_window_for_empty_runner(self):
        self.instance_run_type()

        self.assertNotQVisible(self.run_type.interface.dialog)

        def call_create():
            self.run_type.create()

            QTimer.singleShot(
                10,
                lambda: self.assertQVisible(self.run_type.interface.dialog))

        qtest_helpers.button_callback(
            method=call_create, button=self.ok_button)

        self.assertNotQVisible(self.run_type.interface.dialog)

    def test_run_empty_runner(self):
        self.runner = MM()
        self.instance_run_type()

        qtest_helpers.button_callback(
            method=self.run_type.create, button=self.ok_button)

        self.runner.assert_called_once_with({
            'key': 'My Default',
            'another_key': 'My Other Default'
        })

    @unittest.skip('expected failure')
    def test_dialog_window_test_behaviour(self):
        # interface can be accepted
        # - window title
        # - validation
        # - reset values
        # - multiple initialisations same widget
        # - converting to values
        assert False
