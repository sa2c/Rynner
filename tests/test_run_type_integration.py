import unittest
from unittest.mock import MagicMock as MM
from rynner.run_type import RunType, RunAction
from rynner.inputs import Interface, TextInput, RunnerConfigDialog
from tests.qtest_helpers import QTestCase
from PySide2.QtTest import QTest


class TestRunTypeIntegration(unittest.TestCase):
    @unittest.skip('expected failure')
    # workaround: unittest.expectedFailure does not work with nose
    def test_configure_and_run_empty_runner(self):
        interface = Interface([
            TextInput('key', 'My Label', default="My Default"),
            TextInput(
                'another_key', 'My Other Label', default="My Other Default"),
        ])

        runner = lambda data: None
        some_action = lambda data: None

        run_type = RunType(runner, interface)

        run_type.add_action('Some Action', some_action)

        run_type.create()

        # The dialog window not created (unless in pdb) - need a test for this.
        assert False

    @unittest.skip('expected failure')
    def test_dialog_window_has_title(self):
        assert False

    @unittest.skip('expected failure')
    def test_dialog_window_test_behaviour_title(self):
        # - validation
        # - reset values
        # - multiple initialisations same widget
        # - converting to values
        assert False
