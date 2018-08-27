from PySide2 import QtWidgets
from PySide2.QtWidgets import QPushButton
from rynner.main import MainView
from rynner.behaviour import Behaviour
from rynner.plugin import Plugin, PluginCollection
from rynner.option_maps import slurm1711_option_map as option_map
from rynner.host import Host, Connection
from rynner.logs import Logger
from rynner.create_view import RunCreateView, TextField
from unittest.mock import MagicMock as MM
import pytest

defaults = []


@pytest.fixture
def patched_ssh():
    patcher = patch('rynner.host.paramiko.SSHClient')
    paramiko_mock = self.patcher.start()
    yield paramiko_mock
    patcher.stop()


def plugins():
    plugins = {}
    plugins['rcv0'] = RunCreateView(
        [TextField('param0', 'Parameter 0', default='Some default value 0')])
    plugins['rcv1'] = RunCreateView(
        [TextField('param1', 'Parameter 1', default='Some default value 1')])

    plugins['view_keys1'] = ("id", "name", "some-other-data"),

    plugins['runner0'] = MM()
    plugins['runner1'] = MM()

    # create Plugin objects
    plugins['rt0'] = Plugin(
        'swansea.ac.uk/1',
        'My First Type',
        plugins['rcv0'],
        runner=plugins['runner0'])
    plugins['rt1'] = Plugin(
        'swansea.ac.uk/2',
        'My Second Type',
        plugins['rcv1'],
        view_keys=plugins['view_keys1'],
        runner=plugins['runner1'])

    plugins['plugins'] = [plugins['rt0'], plugins['rt1']]

    return plugins


@pytest.fixture
def host():
    # Set up some hosts
    behaviour = Behaviour(option_map, 'submit_cmd', defaults)
    connection = Connection(
        Logger(),
        'hawklogin.cf.ac.uk',
        user='s.mark.dawson',
        rsa_file='/Users/phoebejoannamay/.ssh/id_rsa')
    datastore = MM()
    return [Host(behaviour, connection, datastore)]


def main_view(qtbot, host, plugins):
    main = MainView(host, plugins)
    qtbot.addWidget(main)
    main.show()
    return main


def select_tab(main, tab=1):
    main.tabs.setCurrentIndex(tab)
    tab = main.tabs.currentWidget()
    return tab


def new_job_window(tab, qtbot):
    qtbot.waitUntil(lambda: tab.isVisible())
    button = find_QPushButton(tab, 'new')
    button.click()
    return visible_config(qtbot, RunCreateView)


def click_button(widget, text):
    ok = find_QPushButton(widget, text)
    ok.click()


def find_QPushButton(widget, text):
    for child in widget.findChildren(QPushButton):
        if child.text().lower() == text.lower():
            if child.isVisible():
                return child

    return None


def window_list(qtbot):
    return QtWidgets.QApplication.topLevelWidgets()


def window_count(qtbot):
    return len(window_list(qtbot))


def visible_config(qtbot, klass):

    plugin_win = [
        w for w in window_list(qtbot)
        if isinstance(w, klass) and w.isVisible()
    ]

    currnumwin = len(plugin_win)

    if (currnumwin != 1):
        raise Exception('duplicate windows')

    return plugin_win[0]


def test_call_first_runner(qtbot):
    p = plugins()
    main = main_view(qtbot, host(), p['plugins'])
    tab = select_tab(main, 0)
    config_window = new_job_window(tab, qtbot)

    # no runners called before ok
    assert not p['rt0'].runner.called
    assert not p['rt1'].runner.called

    # one runner called after ok
    click_button(config_window, 'ok')
    p['rt0'].runner.assert_called_once_with({'param0': 'Some default value 0'})
    assert not p['rt1'].runner.called


def test_call_second_runner(qtbot):
    p = plugins()
    main = main_view(qtbot, host(), p['plugins'])
    tab = select_tab(main, 1)
    config_window = new_job_window(tab, qtbot)

    # config window is visible
    assert config_window.isVisible()

    # no runners called before ok
    assert not p['rt0'].runner.called
    assert not p['rt1'].runner.called

    # one runner called after ok
    click_button(config_window, 'ok')
    p['rt1'].runner.assert_called_once_with({'param1': 'Some default value 1'})
    assert not p['rt0'].runner.called

    # config window has been closed
    assert not config_window.isVisible()


def test_cancel_run(qtbot):
    p = plugins()
    main = main_view(qtbot, host(), p['plugins'])
    tab = select_tab(main, 1)
    config_window = new_job_window(tab, qtbot)

    # window is visible
    assert config_window.isVisible()

    click_button(config_window, 'cancel')

    # window has been closed
    assert not config_window.isVisible()

    # no runners called before ok
    assert not p['rt0'].runner.called
    assert not p['rt1'].runner.called


@pytest.mark.xfail(reason="PluginCollection missing create")
def test_with_runner(qtbot):
    p = plugins()
    allp = [PluginCollection("All", p['plugins']), *p['plugins']]

    main = main_view(qtbot, host(), allp)

    # tab 1 has an ok button
    tab = select_tab(main, 1)
    ok_button = find_QPushButton(tab, 'new')
    assert ok_button is None

    # tab 0 does not
    tab = select_tab(main, 0)
    ok_button = find_QPushButton(tab, 'new')
    assert ok_button is None

    # def runner(data):
    #     a = Run(
    #         nodes=10,
    #         memory=10000,
    #         host=self.hosts[0],
    #         script='my_command')

    #     job_id.append(a.id)

    # # create mock of jobs returned by datastore
    # jobs = {
    #     rt1.domain: [{
    #         'id': '1',
    #         'name': 'JobType1-1',
    #         'some-data': 'Some Data'
    #     }, {
    #         'id': '2',
    #         'name': 'JobType1-2',
    #         'some-data': 'Some Extra Data'
    #     }],
    #     rt2.domain: [{
    #         'id': '1',
    #         'name': 'JobType2-1',
    #         'some-other-data': 'Other Data'
    #     }, {
    #         'id': '2',
    #         'name': 'JobType2-2',
    #         'some-other-data': 'Other Data'
    #     }]
    # }

    # def jobsf(plugin=None):
    #     return jobs[plugin]

    # self.datastore.jobs = jobsf