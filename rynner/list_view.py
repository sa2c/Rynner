from PySide2.QtWidgets import QWidget, QVBoxLayout, QTableView, QTableWidgetItem, QDialog, QAbstractItemView, QTabWidget, QPushButton, QHBoxLayout, QAbstractItemView
import collections
from PySide2.QtCore import QAbstractTableModel, Qt, QObject
from PySide2.QtGui import QStandardItemModel, QStandardItem
from rynner.run_type import RunType


class RynnerListView(QTableView):
    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.setModel(model)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)


class RynnerTableModel(QStandardItemModel):
    def __init__(self, run_type, hosts, parent=None):
        # TODO throw error if all run_type don't have params

        super().__init__(parent)
        self.hosts = hosts

        self.params = run_type.params
        labels = [v[1] for v in self.params]
        self.setHorizontalHeaderLabels(labels)

        self.run_type = run_type

    # TODO - this should be a slot that is connected to by datastore??
    def update(self):
        jobs = self.run_type.list_jobs(self.hosts)
        for col, key_tuple in enumerate(self.run_type.params):
            key, value = key_tuple
            for row, job in enumerate(jobs):
                value = job[key]
                self.setItem(row, col, QStandardItem(value))


class MainView(QDialog):
    '''
    Periodically, for each host, we should fetch a job list of the data visible
    (e.g. from the datastore of the job) for all jobs of the currently visible
    type. Jobs of a given type can be deduced by using their entry in RunType
    (i.e. something like a URL)

    Upshot -> RunType needs a URL + a label
    jobs = [ host.get_jobs(type=run_type.uid) for host in hosts ].flatten()
    '''

    def __init__(self, hosts, run_types):
        super().__init__(None)

        self.hosts = hosts
        self.run_types = run_types

        self.tabs = QTabWidget()
        self.resize(800, 600)

        for run_type in run_types:
            self.add_run_type(run_type)

        self.update_current()

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.tabs)

        # lists are only populated/updated the first time they're seen
        self.tabs.currentChanged.connect(self.update_current)

    def add_run_type(self, run_type):
        widget = QWidget()
        widget.tablemodel = RynnerTableModel(run_type, self.hosts)
        list_view = RynnerListView(widget.tablemodel)
        list_view.setEditTriggers(QAbstractItemView.NoEditTriggers)

        widget.setLayout(QVBoxLayout())
        widget.layout().addWidget(list_view)
        widget.layout().addWidget(QPushButton("New Job"))

        # set headers...
        self.tabs.addTab(widget, run_type.name)

    def update_current(self):
        model = self.tabs.currentWidget().tablemodel
        model.update()
