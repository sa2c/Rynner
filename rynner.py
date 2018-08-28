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

#---------------------------------------------------------
# PLUGIN SCRIPT
#---------------------------------------------------------

# Create a fake run_create_view
view1 = RunCreateView(
    [TextField('Message', 'message', default='Hello, World!')])


def runner(data):
    run = Run(
        ntasks=1,
        memory_per_task_MB=10000,
        host=hosts[0],
        script='echo "Hello from Sunbird!" > "my-job-output"')


# create Plugin objects
plugin1 = Plugin('swansea.ac.uk/1', 'Hello, World!', view1, runner)

#---------------------------------------------------------
# PLUGIN 2 SCRIPT
#---------------------------------------------------------

view2 = RunCreateView([
    TextField('Velocity', 'velocity', default="10"),
    TextField('Altitude', 'altitude', default="40,000"),
    TextField('Angle', 'angle', default='10'),
])

plugin2 = Plugin(
    'swansea.ac.uk/2',
    'simpleCFD',
    view2,
    runner,
    view_keys=("id", "name", "some-other-data"))

#---------------------------------------------------------
# INITIALISATION
#---------------------------------------------------------

# Set up some hosts
import re
pid_from_stdout = re.compile('Submitted batch job (?P<id>[0-9]+)')

behaviour = Behaviour(option_map, 'sbatch {jobcard}', pid_from_stdout,
                      defaults)

rsa_file = f'{homedir}/.ssh/id_rsa'
print(f'rsa file: {rsa_file}')
print('connecting')
connection = Connection(
    Logger(), 'hawklogin.cf.ac.uk', user='s.mark.dawson', rsa_file=rsa_file)
datastore = MM()
hosts = [Host(behaviour, connection, datastore)]

print('define rynner')

print('create plugins')

plugins = [PluginCollection("All Runs", [plugin1, plugin2]), plugin1, plugin2]

# create mock of jobs returned by datastore
jobs = {
    plugin1.domain: [{
        'id': '12508',
        'name': 'JobType1-1',
        'some-data': 'Some Data'
    }, {
        'id': '23045',
        'name': 'JobType1-2',
        'some-data': 'Some Extra Data'
    }],
    plugin2.domain: [{
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
