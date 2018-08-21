import unittest
from PySide2.QtCore import QTimer
from unittest.mock import MagicMock as MM
from rynner.run_type import RunType, RunAction
from rynner.inputs import Interface, TextField, RunnerConfigDialog
from tests import qtest_helpers
from rynner.run import Run, HostNotSpecifiedException
from rynner.host import Host, Connection
from rynner.behaviour import Behaviour
from PySide2.QtTest import QTest


class TestRunTypeIntegration(qtest_helpers.QTestCase):
    def setUp(self):
        self.interface = Interface([
            TextField('key', 'My Label', default="My Default"),
            TextField(
                'another_key', 'My Other Label', default="My Other Default"),
        ])
        self.runner = lambda data: None

    def instance_run_type(self):
        self.run_type = RunType(self.runner, self.interface)
        button_box = self.run_type.interface.dialog._button_box
        self.ok_button = qtest_helpers.get_button(button_box, 'ok')
        self.cancel_button = qtest_helpers.get_button(button_box, 'cancel')

    def test_show_config_window_for_empty_runner(self):
        '''
        show the dialog box on run_type.create, hide on click OK
        '''
        self.instance_run_type()

        self.assertNotQVisible(self.run_type.interface.dialog)

        def call_create():
            self.assertQVisible(self.run_type.interface.dialog)
            self.ok_button.click()
            self.assertNotQVisible(self.run_type.interface.dialog)

        QTimer.singleShot(10, call_create)

        self.run_type.create()

    def test_dismiss_on_cancel(self):
        '''
        show the dialog box on run_type.create, hide on click cancel
        '''
        self.instance_run_type()

        def call_create():
            self.assertQVisible(self.run_type.interface.dialog)
            self.cancel_button.click()
            self.assertNotQVisible(self.run_type.interface.dialog)

        QTimer.singleShot(10, call_create)

        self.run_type.create()

    def test_run_empty_runner(self):
        self.runner = MM()
        self.instance_run_type()

        qtest_helpers.button_callback(
            method=self.run_type.create, button=self.ok_button)

        self.runner.assert_called_once_with({
            'key': 'My Default',
            'another_key': 'My Other Default'
        })

    def test_throws_error_without_host(self):
        interface = Interface([
            TextField('Some Parameter', 'param', default='Some default value')
        ])

        connection = MM()

        def runner(self):
            datastore = MM()
            defaults = []
            option_map = [('#FAKE num_nodes={}', 'nodes'), ('#FAKE memory={}',
                                                            'memory')]

            behaviour = Behaviour(option_map, defaults)

            a = Run(
                nodes=10,
                memory=10000,
                host=Host(behaviour, connection, datastore),
                script='my_command')

        rt = RunType(runner, interface)

        button = qtest_helpers.get_button(rt.interface.dialog._button_box,
                                          'ok')
        qtest_helpers.button_callback(method=rt.create, button=button)

        connection.put_file_content.assert_called_once_with(
            'jobcard', '#FAKE num_nodes=10\n#FAKE memory=10000\nmy_command\n')

    @unittest.skip('expected failure')
    def test_dialog_window_test_behaviour(self):
        # interface can be accepted
        # - window title
        # - validation
        # - reset values
        # - multiple initialisations same widget
        # - converting to values
        assert False
