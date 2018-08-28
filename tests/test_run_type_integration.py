import unittest
import pytest
from PySide2.QtCore import QTimer
from PySide2.QtWidgets import *
from unittest.mock import MagicMock as MM
from rynner.plugin import Plugin, RunAction
from rynner.create_view import RunCreateView, TextField
from tests import qtest_helpers
from rynner.run import Run, HostNotSpecifiedException
from rynner.host import Host, Connection
from rynner.behaviour import Behaviour
from PySide2.QtTest import QTest


class TestPluginIntegration(qtest_helpers.QTestCase):
    def setUp(self):
        self.widgets = [
            TextField('key', 'My Label', default="My Default"),
            TextField(
                'another_key', 'My Other Label', default="My Other Default"),
        ]
        self.run_create_view = RunCreateView(self.widgets)
        self.runner = lambda data: None
        self.domain = 'swansea.ac.uk'
        self.type_name = 'My Run Type'

    def instance(self):
        self.plugin = Plugin(self.domain, self.type_name, self.run_create_view,
                             self.runner)

        # find all buttons in
        view = self.plugin.create_view

        self.ok_button = qtest_helpers.find_QPushButton(view, 'ok')
        self.cancel_button = qtest_helpers.find_QPushButton(view, 'cancel')

    def test_show_config_window_for_empty_runner(self):
        '''
        show the dialog box on plugin.create, hide on click OK
        '''
        self.instance()

        self.assertNotQVisible(self.plugin.create_view)

        def call_create():
            self.assertQVisible(self.plugin.create_view)
            self.ok_button.click()
            self.assertNotQVisible(self.plugin.create_view)

        QTimer.singleShot(10, call_create)

        self.plugin.create()

    def test_dismiss_on_cancel(self):
        '''
        show the dialog box on plugin.create, hide on click cancel
        '''
        self.instance()

        def call_create():
            self.assertQVisible(self.plugin.create_view)
            self.cancel_button.click()
            self.assertNotQVisible(self.plugin.create_view)

        QTimer.singleShot(10, call_create)

        self.plugin.create()

    @pytest.mark.xfail(
        reason='do I need to wait for window to get created here?')
    def test_run_empty_runner(self):
        self.runner = MM()
        self.instance()

        qtest_helpers.button_callback(
            method=self.plugin.create, button=self.ok_button)

        self.runner.assert_called_once_with({
            'key': 'My Default',
            'another_key': 'My Other Default'
        })

    @pytest.mark.xfail(reason='known failure, reason no known. timing?')
    def test_throws_error_without_host(self):
        run_create_view = RunCreateView([
            TextField('Some Parameter', 'param', default='Some default value')
        ])

        connection = MM()

        # job_id is a hack to get the run id out of the runner function
        job_id = []

        def runner(self):
            datastore = MM()
            defaults = []
            option_map = [('#FAKE num_nodes={}', 'nodes'), ('#FAKE memory={}',
                                                            'memory')]

            behaviour = Behaviour(option_map, 'submit_cmd', defaults)

            a = Run(
                nodes=10,
                memory=10000,
                host=Host(behaviour, connection, datastore),
                script='my_command')

            job_id.append(a.id)

        rt = Plugin(self.domain, self.type_name, run_create_view, runner)

        button = qtest_helpers.find_QPushButton(rt.create_view, 'ok')
        qtest_helpers.button_callback(method=rt.create, button=button)

        connection.put_file_content.assert_called_once_with(
            '#FAKE num_nodes=10\n#FAKE memory=10000\nmy_command\n',
            f'{job_id[0]}/jobcard')
        connection.run_command.assert_called_once_with(
            'submit_cmd', pwd=f'{job_id[0]}')

    @unittest.skip('expected failure')
    def test_dialog_window_test_behaviour(self):
        # run_create_view can be accepted
        # - window title
        # - validation
        # - reset values
        # - multiple initialisations same widget
        # - converting to values
        assert False
