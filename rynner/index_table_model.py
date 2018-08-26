from PySide2.QtCore import *
from PySide2.QtGui import *


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
                self.setItem(row, col, QStandardItem(value))

#     @Slot()
#     def create_new_run(self):
#         self.plugin.create()

#     @Slot()
#     def stop_run(self, indicies):
#         print(f"stop {self.plugin.name} job {indicies}....!")

#     @Slot()
#     def run_action(self, action, job):
#         print(f"running action f{action} for {self.plugin.name} on {job}")

#     @Slot()
#     def archive_job(self, job):
#         print(f"archiving job f{job} for {self.plugin.name}")

#     # TODO - this should be a slot that is connected to by datastore??
