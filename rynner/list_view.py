from abc import ABC, abstractmethod
from PySide2.QtWidgets import QWidget, QVBoxLayout, QTableView, QTableWidgetItem, QDialog, QAbstractItemView, QTabWidget, QPushButton, QHBoxLayout, QAbstractItemView, QComboBox, QLabel, QSpacerItem, QSizePolicy, QItemDelegate
import collections
from PySide2.QtCore import QAbstractTableModel, Qt, QObject, Signal
from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtQuick import QQuickView
from PySide2.QtCore import QUrl
from rynner.run_type import Plugin, RunAction
from rynner.ui import load_ui


# TODO - No unit tests for code in this file
class RynnerTabSignals(QObject):
    new_run = Signal()
    stop_run = Signal()
    run_action = Signal(RunAction)


class RynnerTableModel(QStandardItemModel):
    def __init__(self, run_type, hosts, parent=None):
        # TODO throw error if all run_type don't have view_keys

        super().__init__(parent)
        self.hosts = hosts

        self.view_keys = run_type.view_keys
        labels = [v[1] for v in self.view_keys]
        self.setHorizontalHeaderLabels(labels)

        self.run_type = run_type

        self.refresh_from_datastore()

    # TODO - this should be a slot that is connected to by datastore??
    def refresh_from_datastore(self):
        jobs = self.run_type.list_jobs(self.hosts)
        for col, key in enumerate(self.run_type.view_keys):
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
    jobs = [ host.get_jobs(type=run_type.uid) for host in hosts ].flatten()
    '''

    def __init__(self, hosts, run_types):
        super().__init__(None)

        self.hosts = hosts
        self.run_types = run_types

        self.tabs = QTabWidget()
        self.resize(800, 600)

        # Add a new tab for each run type
        models = {}
        for run_type in run_types:
            models[run_type] = RynnerTableModel(run_type, hosts)
            if run_type.build_index_view is not None:
                view = run_type.build_index_view(models[run_type], run_type)
            else:
                # TODO - passing run_type in here is dubious at best...
                # maybe pass be a proxy object with a bunch of slots?
                view = build_index_view(models[run_type], run_type)

            self.tabs.addTab(view, run_type.name)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.tabs)

    def create_new_job(self):
        if len(self.tableview.run_types) == 1:
            self.tableview.run_types[0].create()
        else:
            raise NotImplementedException()
            #run_type = QPluginSelector(self.tableview.run_types)


# takes in the table model and returns a view widget! with links signals?
# contains run_type so that signals can be linked?? Maybe I need a run type proxy??
def build_index_view(model, run_type):
    # could potentially also just put it in the right place??
    view = load_ui('list_view.ui')

    # create the a table view and model

    view.table.setModel(model)
    # can probably set these in view
    view.table.setSelectionBehavior(QAbstractItemView.SelectRows)
    view.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

    if hasattr(run_type, 'create'):
        view.newButton.clicked.connect(run_type.create)
    else:
        view.newButton.setVisible(False)
        view.stopButton.setVisible(False)

        # TODO - also need to set up view here

    return view

    def create_new_job(self):
        if len(self.tableview.run_types) == 1:
            self.tableview.run_types[0].create()
        else:
            raise NotImplementedException()
            #run_type = QPluginSelector(self.tableview.run_types)

    def cancel_job(self):
        print('Cancel Job')


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
