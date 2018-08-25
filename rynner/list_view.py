from abc import ABC, abstractmethod
from PySide2.QtWidgets import QWidget, QVBoxLayout, QTableView, QTableWidgetItem, QDialog, QAbstractItemView, QTabWidget, QPushButton, QHBoxLayout, QAbstractItemView, QComboBox, QLabel, QSpacerItem, QSizePolicy, QItemDelegate
import collections
from PySide2.QtCore import QAbstractTableModel, Qt, QObject, Signal
from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtQuick import QQuickView
from PySide2.QtCore import QUrl, Slot
from rynner.plugin import Plugin, RunAction
from rynner.ui import load_ui


class RynnerTableModel(QStandardItemModel):
    def __init__(self, plugin, hosts, parent=None):
        # TODO throw error if all plugin don't have view_keys

        super().__init__(parent)
        self.hosts = hosts

        self.view_keys = plugin.view_keys
        self.setHorizontalHeaderLabels(self.view_keys)

        self.plugin = plugin

        self.refresh_from_datastore()

    @Slot()
    def create_new_run(self):
        print(f"create {self.plugin.name}....!")


    @Slot()
    def stop_run(self, model_index):
        run = model_index.row()
        print(f"stop {self.plugin.name} job {run}....!")

    @Slot()
    def run_action(self, action, job):
        print(f"running action f{action} for {self.plugin.name} on {job}")

    @Slot()
    def archive_job(self, job):
        print(f"archiving job f{job} for {self.plugin.name}")

    # TODO - this should be a slot that is connected to by datastore??
    def refresh_from_datastore(self):
        jobs = self.plugin.list_jobs(self.hosts)
        for col, key in enumerate(self.plugin.view_keys):
            for row, job in enumerate(jobs):
                value = job[key]
                self.setItem(row, col, QStandardItem(value))


class MainView(QDialog):
    '''
    Periodically, for each host, we should fetch a job list of the data visible
    (e.g. from the datastore of the job) for all jobs of the currently visible
    type. Jobs of a given type can be deduced by using their entry in Plugin
    (i.e. something like a URL)

    Upshot -> Plugin needs a URL + a label
    jobs = [ host.get_jobs(type=plugin.uid) for host in hosts ].flatten()
    '''

    def __init__(self, hosts, plugins):
        super().__init__(None)

        self.hosts = hosts
        self.plugins = plugins

        self.tabs = QTabWidget()
        self.resize(800, 600)

        # Add a new tab for each run type
        models = {}
        for plugin in plugins:
            models[plugin] = RynnerTableModel(plugin, hosts)
            if plugin.build_index_view is not None:
                view = plugin.build_index_view(models[plugin])
            else:
                # TODO - passing plugin in here is dubious at best...
                # maybe pass be a proxy object with a bunch of slots?
                view = build_index_view(models[plugin], 'list_view.ui')

            self.tabs.addTab(view, plugin.name)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.tabs)


# takes in the table model and returns a view widget! with links signals?
# contains plugin so that signals can be linked?? Maybe I need a run type proxy??
def build_index_view(model, ui_file):
    # could potentially also just put it in the right place??
    view = load_ui(ui_file)

    # create the a table view and model

    view.table.setModel(model)
    # can probably set these in view
    view.table.setSelectionBehavior(QAbstractItemView.SelectRows)
    view.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

    # add actions
    view.actionComboBox.addItem("action")

    view.newButton.clicked.connect(model.create_new_run)
    view.stopButton.clicked.connect(lambda selected : model.stop_run(view.table.currentIndex()))

    def set_action(action_idx):
        job_idx = view.table.currentIndex()
        if action_idx > 0:
            model.run_action(action_idx, job_idx)
        view.actionComboBox.setCurrentIndex(0)

    view.actionComboBox.currentIndexChanged.connect(set_action)
    # TODO - also need to set up view here

    return view


class QActionSelector(QWidget):
    def __init__(self, actions, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        self.setLayout(layout)

        if len(actions) > 0:
            layout.addWidget(QLabel("Run Action: "))
            combo = QComboBox()

            combo.addItem("Select action...")

            for action in actions:
                combo.addItem(action.label)

            layout.addWidget(combo)
