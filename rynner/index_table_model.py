from PySide2.QtCore import *
from PySide2.QtGui import *
from rynner.plugin import RunAction

class InvalidModelIndex(Exception):
    pass

class IndexTableModel(QStandardItemModel):
    '''
    Public API:
    self.plugin : the plugin instance to display
    self.view_keys : the keys from the plugin to display
    '''

    def __init__(self, plugin, parent=None):
        super().__init__(parent)
        # TODO should handle a plugin which has no "view_keys" property
        self.plugin = plugin

        self.setHorizontalHeaderLabels(plugin.view_keys)

        self.plugin.runs_changed.connect(self.update_jobs)

    @Slot()
    def update_jobs(self):
        jobs = self.plugin.list_jobs()

        for col, key in enumerate(self.plugin.view_keys):
            for row, job in enumerate(jobs):
                value = job[key]
                item = QStandardItem(value)
                self.setItem(row, col, item)
                if col == 0:
                    item.setData(job, Qt.UserRole)

    @Slot()
    def create_new_run(self):
        self.plugin.create()

    @Slot(QModelIndex)
    def stop_run(self, model_index):
        run_data = self._run_id_from_model_index(model_index)
        self.plugin.stop_run(run_data)

    @Slot(RunAction, QModelIndex)
    def run_action(self, action, model_index):
        run_data = self._run_id_from_model_index(model_index)
        action.run(run_data)

    def _run_id_from_model_index(self, model_index):
        if not model_index.isValid():
            raise InvalidModelIndex(f'model index not found {model_index}')

        model_index_data = self.index(model_index.row(), 0)
        data = self.data(model_index_data, Qt.UserRole)
        return data
