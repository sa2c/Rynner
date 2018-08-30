import os, glob
from unittest.mock import patch, call, ANY
from unittest.mock import MagicMock as MM
from tests.qtest_helpers import *
import rynner
from rynner.datastore import Datastore
from rynner.option_parser import OptionParser
from rynner.main import MainView
from rynner.create_view import RunCreateView, TextField
from rynner.plugin import Plugin, PluginCollection, RunAction
from rynner.run import RunManager
from rynner.host_patterns import slurm1711_host_pattern as host_pattern
from rynner.logs import Logger
from tests.host_env import *

defaults = []

#---------------------------------------------------------
# PLUGIN SCRIPT
#---------------------------------------------------------

# Create a fake run_create_view
view1 = RunCreateView(
    [TextField('Message', 'message', default='Hello, World!')])


def runner(run_manager, data):
    run = run_manager.new(
        ntasks=1,
        memory_per_task_MB=10000,
        host=hosts[0],
        script='echo "Hello from Sunbird!" > "my-job-output"')


# create Plugin objects
plugin1 = Plugin(
    'swansea.ac.uk/1',
    'Hello, World!',
    view1,
    runner,
    view_keys=[
        ('Message', 'config-options.Message'),
    ])

#---------------------------------------------------------
# PLUGIN 2 SCRIPT
#---------------------------------------------------------

view2 = RunCreateView([
    TextField('Velocity', 'velocity', default="10"),
    TextField('Altitude', 'altitude', default="40,000"),
    TextField('Angle', 'angle', default='10'),
])


def runner2(run_manager, data):
    print('running...')


plugin2 = Plugin(
    'swansea.ac.uk/2',
    'simpleCFD',
    view2,
    runner2,
    view_keys=[
        ('Velocity', 'config-options.Velocity'),
    ])
#---------------------------------------------------------
# INITIALISATION
#---------------------------------------------------------

# submit the job and write output to
submit_cmd = 'echo 1234 > jobid'
# Set up some hosts

rsa_file = f'{homedir}/.ssh/id_rsa'
hosts = [SlurmHost(identifier)]

print('create plugins')

plugins = [PluginCollection("All Runs", [plugin1, plugin2]), plugin1, plugin2]


def update_plugins():
    print('update')
    for plugin in [plugin1, plugin2]:
        plugin_id = plugin.plugin_id
        for host in hosts:
            host.update(plugin_id)


timer = QTimer()
timer.timeout.connect(update_plugins)
secs = 1
timer.start(secs * 1000)
QTimer.singleShot(10, update_plugins)

main = MainView(hosts, plugins)
main.show()
app.exec_()
