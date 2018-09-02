import os, glob
import yaml
from unittest.mock import patch, call, ANY
from unittest.mock import MagicMock as MM
from tests.qtest_helpers import *
import rynner.host
from rynner.datastore import Datastore
from rynner.pattern_parser import PatternParser
from rynner.main import MainView
from rynner.create_view import RunCreateView, TextField
from rynner.plugin import Plugin, PluginCollection, RunAction
from rynner.run import RunManager
from rynner.host_patterns import host_patterns
from rynner.logs import Logger
from tests.host_env import *

defaults = []

#---------------------------------------------------------
# PLUGIN SCRIPT
#---------------------------------------------------------

# Create a fake run_create_view
view1 = [TextField('Message', 'message', default='Hello, World!')]


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
        ('State', 'queue.State'),
        ('Elapsed', 'queue.Elapsed'),
        ('Time Limit', 'queue.TimeLimit'),
    ])

#---------------------------------------------------------
# PLUGIN 2 SCRIPT
#---------------------------------------------------------

view2 = [
    TextField('Velocity', 'velocity', default="10"),
    TextField('Altitude', 'altitude', default="40,000"),
    TextField('Angle', 'angle', default='10'),
]


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
# LOAD HOSTS
#---------------------------------------------------------

globdir = f'{homedir}/.rynner/hosts/*'
host_config_files = glob.glob(globdir)

if len(host_config_files) == 0:
    raise Exception(f'No host config files found in {globdir}')

hosts = []

for filename in host_config_files:
    with open(filename, 'r') as file:
        host_config = yaml.load(file)
    host_class = getattr(rynner.host, host_config['classname'])
    host = host_class(host_config['domain'], host_config['username'],
                      host_config['rsa_file'])
    hosts.append(host)

#---------------------------------------------------------
# INITIALISE PLUGINS
#---------------------------------------------------------

plugins = [PluginCollection("All Runs", [plugin1, plugin2]), plugin1, plugin2]

#---------------------------------------------------------
# Run application
#---------------------------------------------------------


def update_plugins():
    for plugin in [plugin1, plugin2]:
        plugin_id = plugin.plugin_id
        for host in hosts:
            host.update(plugin_id)


timer = QTimer()
timer.timeout.connect(update_plugins)
secs = 60
timer.start(secs * 1000)
QTimer.singleShot(10, update_plugins)

main = MainView(hosts, plugins)
main.show()
app.exec_()
