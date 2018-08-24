from PySide2.QtWidgets import QWidget, QVBoxLayout, QTableView, QTableWidgetItem, QDialog, QAbstractItemView, QTabWidget, QPushButton, QHBoxLayout, QAbstractItemView, QComboBox, QLabel, QSpacerItem, QSizePolicy, QItemDelegate
import collections
from PySide2.QtCore import QAbstractTableModel, Qt, QObject
from PySide2.QtGui import QStandardItemModel, QStandardItem
from rynner.run_type import RunType
from rynner.ui import load_ui

# TODO - No unit tests for code in this file


class RynnerTableModel(QStandardItemModel):
    def __init__(self, run_type, hosts, parent=None):
        # TODO throw error if all run_type don't have params

        super().__init__(parent)
        self.hosts = hosts

        self.params = run_type.params
        labels = [v[1] for v in self.params]
        self.setHorizontalHeaderLabels(labels)

        self.run_type = run_type

        self.refresh_from_datastore()

    # TODO - this should be a slot that is connected to by datastore??
    def refresh_from_datastore(self):
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

        # Add a new tab for each run type
        for run_type in run_types:
            new_tab = QRunTypeView(run_type, hosts)

            self.tabs.addTab(new_tab, run_type.name)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.tabs)


class QRunTypeView(QWidget):
    def __init__(self, run_type, hosts, parent=None, view=None):
        super().__init__(parent)
        if view is None:
            # could potentially also just put it in the right place??
            view = load_ui('list_view.ui')

        # create the a table view and model
        self.tablemodel = RynnerTableModel(run_type, hosts)

        view.tableView.setModel(self.tablemodel)
        # can probably set these in view
        view.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        view.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(view)

        #button_container = QWidget()
        #cancel_job_button = QPushButton("Cancel Job")
        #new_job_button = QPushButton("New Job")
        #action_control = QActionSelector(run_type.actions)
        #layout = QHBoxLayout()
        #layout.addWidget(new_job_button)
        #layout.addWidget(cancel_job_button)
        #layout.addItem(
        #    QSpacerItem(10, 10, QSizePolicy.MinimumExpanding,
        #                QSizePolicy.Expanding))
        #layout.addWidget(action_control)
        #layout.addItem(
        #    QSpacerItem(100, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        #button_container.setLayout(layout)
        #self.layout().addWidget(button_container)

        #new_job_button.clicked.connect(self.create_new_job)
        #cancel_job_button.clicked.connect(self.cancel_job)

    def create_new_job(self):
        if len(self.tableview.run_types) == 1:
            self.tableview.run_types[0].create()
        else:
            raise NotImplementedException()
            #run_type = QRunTypeSelector(self.tableview.run_types)

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
