import unittest
from unittest.mock import patch, call, ANY
from unittest.mock import MagicMock as MM
from rynner.list_view import *
from tests.qtest_helpers import *
from rynner.host import Host, Connection
from rynner.behaviour import Behaviour
from rynner.inputs import Interface, TextField
from rynner.run_type import RunType, RunTypeCollection, RunAction
from rynner.run import Run


class RunView:
    def __init__(self, jobId, JobName, Parameter):
        self.jobId = jobId
        self.jobName = JobName
        self.Parameter = Parameter


class TestRun(unittest.TestCase):
    def setUp(self):

        # Create a fake interface
        self.interface = Interface([
            TextField('Some Parameter', 'param', default='Some default value')
        ])

        option_map = [('#FAKE num_nodes={}', 'nodes'), ('#FAKE memory={}',
                                                        'memory')]
        defaults = []

        # Set up some hosts
        behaviour = Behaviour(option_map, 'submit_cmd', defaults)
        connection = Connection('hawk', 's.mark.dawson')
        self.datastore = MM()
        self.hosts = [Host(behaviour, connection, self.datastore)]

        def runner(data):

            a = Run(nodes=10, memory=10000, host=hosts[0], script='my_command')

            job_id.append(a.id)

        self.runner = runner

        self.action = lambda x: print("TEST")

    def create_run_types(self):

        # create RunType objects
        rt1 = RunType('swansea.ac.uk/1', 'My First Type', self.interface,
                      self.runner)
        rt2 = RunType(
            'swansea.ac.uk/2',
            'My Second Type',
            self.interface,
            self.runner,
            params=[("id", "Job ID"), ("name", "Job Name"),
                    ("some-other-data", "Some Other Value")])

        rt1.add_action("My Action", self.action)

        self.run_types = [rt1, rt2]

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

        def jobsf(run_type=None):
            return jobs[run_type]

        self.datastore.jobs = jobsf

    def test_show_groups(self):
        self.create_run_types()
        run_types = [RunTypeCollection("All", self.run_types)]
        run_types.extend(self.run_types)

        # rt.create()

        # test with single entry + with a list of lists (as type)
        #run_types = [rt_all, rt1, rt2]
        #run_types = [rt1, rt2]

        self.tabs = MainView(self.hosts, run_types)
        self.tabs.exec_()

    def test_show_QRunTypeView(self):
        self.create_run_types()

        q = QRunTypeView(self.run_types[0], self.hosts)
        q.tablemodel.refresh_from_datastore()

        q.show()

    def test_action_selector(self):
        func = lambda x: None
        actions = [
            RunAction('Action 1', func),
            RunAction('Action 2', func),
            RunAction('Action 3', func),
            RunAction('Action 4', func),
        ]
        act_select = QActionSelector(actions)
        act_select.show()
        app.exec_()
