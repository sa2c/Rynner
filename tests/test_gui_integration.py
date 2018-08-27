from PySide2.QtWidgets import QApplication
from rynner.main import MainView
from rynner.option_maps import slurm1711_option_map as option_map
from rynner.create_view import RunCreateView, TextField
from rynner.behaviour import Behaviour
from rynner.plugin import Plugin
from tests.qtest_helpers import find_QPushButton, app
from rynner.host import Host, Connection
from rynner.logs import Logger
import unittest
from unittest.mock import MagicMock as MM

# TODO - this isn't used!
defaults = []


class MainWindowTester():
    def __init__(self, hosts, plugins, log=False):
        self.do_log = log
        self.plugins = plugins
        self.log('creating main')
        self.main = MainView(hosts, plugins)
        self.main.show()
        self.tabs = self.main.tabs

    def current_tab(self):
        return self.tabs.currentWidget()

    def new_job(self):
        self.log('click new job button')
        tab = self.current_tab()
        tab.newButton.click()

    def cancel_config(self):
        self.log('cancelling config')
        cancel_button = find_QPushButton(self.visible_config(), 'cancel')
        cancel_button.click()

    def accept_config(self):
        self.log('start accepting config')
        ok_button = find_QPushButton(self.visible_config(), 'ok')
        ok_button.click()
        print('ok clicked')

    def visible_config(self, match=RunCreateView, numwin=1):
        self.log('finding config window')

        plugin_win = [
            w for w in app.topLevelWidgets()
            if isinstance(w, match) and w.isVisible()
        ]

        currnumwin = len(plugin_win)

        if (currnumwin == numwin):
            return plugin_win[0]
        else:
            raise Exception(
                f'Something probably went wrong: {currnumwin} visible plugin windows found: {plugin_win}'
            )

    def log(self, message):
        if self.do_log:
            print(message)


class TestGuiIntegration(unittest.TestCase):
    def setUp(self):
        self.runner1 = MM()
        self.runner2 = MM()

        self.run_create_view1 = RunCreateView(
            [TextField('param1', 'Parameter 1', default='Some default value')])

        self.run_create_view2 = RunCreateView(
            [TextField('param2', 'Parameter 2', default='Some default value')])

        self.view_keys2 = ("id", "name", "some-other-data"),

        # create Plugin objects
        rt1 = Plugin(
            'swansea.ac.uk/1',
            'My First Type',
            self.run_create_view1,
            runner=self.runner1)
        rt2 = Plugin(
            'swansea.ac.uk/2',
            'My Second Type',
            self.run_create_view2,
            view_keys=self.view_keys2,
            runner=self.runner2)

        self.plugins = [rt1, rt2]

        # Set up some hosts
        self.behaviour = Behaviour(option_map, 'submit_cmd', defaults)
        self.connection = Connection(
            Logger(),
            'hawklogin.cf.ac.uk',
            user='s.mark.dawson',
            rsa_file='/Users/phoebejoannamay/.ssh/id_rsa')
        self.datastore = MM()
        self.hosts = [Host(self.behaviour, self.connection, self.datastore)]

    def test_create_accept_run(self):
        '''
        creates a new run
        '''
        main = MainWindowTester(self.hosts, self.plugins)
        main.new_job()
        main.accept_config()
        self.runner1.assert_called_once_with({'param1': 'Some default value'})
