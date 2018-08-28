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
from rynner.option_maps import slurm1711_option_map as option_map
from rynner.logs import Logger

homedir = os.environ['HOME']

defaults = []

# Create a fake run_create_view
run_create_view1 = RunCreateView(
    [TextField('Message', 'message', default='Hello, World!')])

run_create_view2 = RunCreateView([
    TextField('Velocity', 'velocity', default="10"),
    TextField('Altitude', 'altitude', default="40,000"),
    TextField('Angle', 'angle', default='10'),
])

# Set up some hosts
behaviour = Behaviour(option_map, 'sbatch {jobcard}', defaults)

rsa_file = f'{homedir}/.ssh/id_rsa'
print(f'rsa file: {rsa_file}')
print('connecting')
connection = Connection(
    Logger(), 'hawklogin.cf.ac.uk', user='s.mark.dawson', rsa_file=rsa_file)
datastore = MM()
hosts = [Host(behaviour, connection, datastore)]

print('define rynner')


def runner(data):

    a = Run(
        ntasks=10,
        memory_per_task_MB=10000,
        host=hosts[0],
        script='echo "Hello from Sunbird!" > "my-job-output"')


print('create plugins')

# create Plugin objects
rt1 = Plugin('swansea.ac.uk/1', 'Hello, World!', run_create_view1, runner)
rt2 = Plugin(
    'swansea.ac.uk/2',
    'simpleCFD',
    run_create_view2,
    runner,
    view_keys=("id", "name", "some-other-data"))

plugins = [PluginCollection("All Runs", [rt1, rt2]), rt1, rt2]

# create mock of jobs returned by datastore
jobs = {
    rt1.domain: [{
        'id': '12508',
        'name': 'JobType1-1',
        'some-data': 'Some Data'
    }, {
        'id': '23045',
        'name': 'JobType1-2',
        'some-data': 'Some Extra Data'
    }],
    rt2.domain: [{
        'id': '12435',
        'name': 'JobType2-1',
        'some-other-data': 'Other Data'
    }, {
        'id': '24359',
        'name': 'JobType2-2',
        'some-other-data': 'Other Data'
    }]
}

datastore.jobs = lambda plugin=None: jobs[plugin]

main = MainView(hosts, plugins)

main.show()
app.exec_()
