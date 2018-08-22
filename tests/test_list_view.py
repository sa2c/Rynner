import unittest
from unittest.mock import patch, call, ANY
from unittest.mock import MagicMock as MM
from rynner.list_view import *
from tests.qtest_helpers import *
from rynner.host import Host, Connection
from rynner.behaviour import Behaviour
from rynner.inputs import Interface, TextField
from rynner.run_type import RunType, RunTypeCollection
from rynner.run import Run


class RunView:
    def __init__(self, jobId, JobName, Parameter):
        self.jobId = jobId
        self.jobName = JobName
        self.Parameter = Parameter


class TestRun(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def instantiate(self):
        interface = Interface([
            TextField('Some Parameter', 'param', default='Some default value')
        ])

        defaults = []
        option_map = [('#FAKE num_nodes={}', 'nodes'), ('#FAKE memory={}',
                                                        'memory')]

        behaviour = Behaviour(option_map, 'submit_cmd', defaults)
        connection = Connection('hawk', 's.mark.dawson')
        datastore = MM()

        hosts = [Host(behaviour, connection, datastore)]

        def runner(data):

            a = Run(nodes=10, memory=10000, host=hosts[0], script='my_command')

            job_id.append(a.id)

        rt1 = RunType('swansea.ac.uk/1', 'My First Type', interface, runner)
        rt2 = RunType(
            'swansea.ac.uk/2',
            'My Second Type',
            interface,
            runner,
            params=[("id", "Job ID"), ("name", "Job Name"),
                    ("some-other-data", "Some Other Value")])
        rt_all = RunTypeCollection("All", [rt1, rt2])

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

        datastore.jobs = jobsf

        # rt.create()

        # test with single entry + with a list of lists (as type)
        run_types = [rt_all, rt1, rt2]
        #run_types = [rt1, rt2]

        self.tabs = MainView(hosts, run_types)

    def test_instantiation(self):
        self.instantiate()
        self.tabs.show()
        app.exec_()
