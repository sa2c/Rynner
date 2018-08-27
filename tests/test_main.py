import unittest
import os
from unittest.mock import patch, call, ANY
from unittest.mock import MagicMock as MM
from tests.qtest_helpers import *
from rynner.host import Host, Connection
from rynner.behaviour import Behaviour
from rynner.main import MainView
from rynner.create_view import RunCreateView, TextField
from rynner.plugin import Plugin, PluginCollection, RunAction
from rynner.run import Run


class RunView:
    def __init__(self, jobId, JobName, Parameter):
        self.jobId = jobId
        self.jobName = JobName
        self.Parameter = Parameter


class TestRun(unittest.TestCase):
    def setUp(self):

        # Create a fake run_create_view
        self.run_create_view = RunCreateView([
            TextField('Some Parameter', 'param', default='Some default value')
        ])

        option_map = [('#FAKE num_nodes={}', 'nodes'), ('#FAKE memory={}',
                                                        'memory')]
        defaults = []

        # Set up some hosts
        behaviour = Behaviour(option_map, 'submit_cmd', defaults)

        self.patcher = patch('rynner.host.paramiko.SSHClient')
        self.paramiko_mock = self.patcher.start()

        connection = Connection('hawk', key_filename='keyfile')
        self.datastore = MM()
        self.hosts = [Host(behaviour, connection, self.datastore)]

        def runner(data):

            a = Run(
                nodes=10,
                memory=10000,
                host=self.hosts[0],
                script='my_command')

            job_id.append(a.id)

        self.runner = runner

        self.action = lambda x: print("TEST")

    def tearDown(self):
        self.patcher.stop()

    def create_plugins(self):

        # create Plugin objects
        rt1 = Plugin('swansea.ac.uk/1', 'My First Type', self.run_create_view,
                     self.runner)
        rt2 = Plugin(
            'swansea.ac.uk/2',
            'My Second Type',
            self.run_create_view,
            self.runner,
            view_keys=("id", "name", "some-other-data"))

        rt1.add_action("My Action", self.action)

        self.plugins = [rt1, rt2]

        # create mock of jobs returned by datastore
        jobs = {
            rt1.domain: [{
                'id': '1',
                'name': 'JobType1-1',
                'some-data': 'Some Data'
            }, {
                'id': '2',
                'name': 'JobType1-2',
                'some-data': 'Some Extra Data'
            }],
            rt2.domain: [{
                'id': '1',
                'name': 'JobType2-1',
                'some-other-data': 'Other Data'
            }, {
                'id': '2',
                'name': 'JobType2-2',
                'some-other-data': 'Other Data'
            }]
        }

        def jobsf(plugin=None):
            return jobs[plugin]

        self.datastore.jobs = jobsf

    def test_show_groups(self):
        self.create_plugins()
        plugins = [PluginCollection("All", self.plugins)]
        plugins.extend(self.plugins)

        main = MainView(self.hosts, plugins)
        main.tabs.setCurrentIndex(1)
        current_tab = main.tabs.currentWidget()
        tab_ok_button = find_QPushButton(current_tab, 'new')
        tab_ok_button.click()

        def callback():
            window = QApplication.activeWindow()
            print("***" + str(window))

        QTimer.singleShot(10, callback)

        main.exec_()
