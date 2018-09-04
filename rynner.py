import os, glob
import sys
import yaml
from unittest.mock import patch, call, ANY
from unittest.mock import MagicMock as MM
import rynner.host as host_module
from tests.qtest_helpers import *
from rynner import *
from rynner.plugin import PluginCollection
from tests.host_env import *
from PySide2.QtGui import QIcon

defaults = []
allplugins = []
hosts = []

def update_plugins():
    print('update plugins..')
    for plugin in allplugins:
        print(f'update {plugin}..')
        sys.stdout.flush()
        plugin_id = plugin.plugin_id
        for host in hosts:
            host.update(plugin_id)


#---------------------------------------------------------
# PLUGIN SCRIPT
#---------------------------------------------------------


# Create a fake run_create_view
view1 = [
    TextField('size', 'Temporal Size', default=''),
    TextField('volume', 'Spatial Size', default=''),
    TextField('beta', 'Beta', default=''),
    TextField('m', 'M', default='')
    ]


def runner(run_manager, data):
    run = run_manager.new(
        ntasks=1,
        memory_per_task_MB=10000,
        host=hosts[0],
        script='echo "Hello from Sunbird!" > "my-job-output"')
    update_plugins()


# create Plugin objects
plugin1 = Plugin(
    'swansea.ac.uk/1',
    'Lattice Submission',
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
    host_class = getattr(host_module, host_config['classname'])
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

allplugins.append(plugin1)
allplugins.append(plugin2)

print('start timer')
sys.stdout.flush()
timer = QTimer()
timer.timeout.connect(update_plugins)
secs = 60
timer.start(secs * 1000)
QTimer.singleShot(10, update_plugins)

main = MainView(hosts, plugins)

#---------------------------------------------------------
# Icon
#---------------------------------------------------------

icon = QIcon("icons/Rynner-icon-256.png")
icon.addFile("icons/Rynner-icon-32.png")
main.setWindowIcon(icon)
main.setWindowTitle("Rynner")

#---------------------------------------------------------
# Start
#---------------------------------------------------------

main.show()
app.exec_()
