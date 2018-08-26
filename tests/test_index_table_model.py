import unittest
from PySide2.QtCore import *
from PySide2.QtGui import *
from unittest.mock import MagicMock as MM, patch
from rynner.index_table_model import *
from rynner.plugin import *


class TestIndexTableModel(unittest.TestCase):
    def setUp(self):
        self.plugin = Plugin('some-domain', 'plugin name')

    def instance(self):
        return IndexTableModel(self.plugin)

    def test_instance(self):
        self.instance()

    def test_contains_plugin(self):
        i = self.instance()
        self.assertEqual(i.plugin, self.plugin)

    def test_horizontal_headers(self):
        i = self.instance()
        labels = (i.headerData(j, Qt.Orientation.Horizontal)
                  for j in range(i.columnCount()))
        labels = tuple(labels)
        self.assertEqual(labels, self.plugin.view_keys)

    def test_connects_plugin_to_update_jobs(self):
        self.plugin = MM()
        i = self.instance()
        i.plugin.runs_changed.connect.assert_called_once_with(i.update_jobs)

    def test_correct_row_col_count(self):
        i = self.instance()

        jobs = [ { 'id' : 'My ID', 'name' : 'My Name'} ]
        i.plugin.list_jobs = lambda : jobs
        keys =  ['id', 'name']
        i.plugin.view_keys = keys

        # expected table sizes
        num_cols = len(keys)
        num_rows = len(jobs)

        # model empty before
        self.assertEqual(i.columnCount(), num_cols)
        self.assertEqual(i.rowCount(), 0)

        i.update_jobs()

        self.assertEqual(i.columnCount(), num_cols)
        self.assertEqual(i.rowCount(), num_rows)

    def test_connects_plugin_to_update_jobs(self):
        i = self.instance()
        jobs = [ { 'id' : 'My ID', 'name' : 'My Name'} ]
        keys = i.plugin.view_keys
        i.plugin.list_jobs = lambda : jobs

        # expected table sizes
        num_cols = len(keys)
        num_rows = len(jobs)

        i.update_jobs()

        for row in range(num_rows):
            for col in range(num_cols):
                job = jobs[row]
                key = keys[col]
                item = i.item(row, col)
                self.assertEqual(item.text(), job[key])


class TestRefreshFromDatastore(TestIndexTableModel):
    def test_gets_jobs_from_list_jobs(self):
        self.plugin = MM()
        i = self.instance()
        self.assertFalse(self.plugin.list_jobs.called)
        i.update_jobs()
        self.assertTrue(self.plugin.list_jobs.called)


if __name__ == '__main__':
    unittest.main()
