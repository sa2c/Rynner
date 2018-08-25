import unittest
from unittest.mock import MagicMock as MM
from rynner.run_manager import RunManager


class TestRunManager(unittest.TestCase):
    def setUp(self):
        self.hosts = [MM(), MM()]
        self.plugins = [MM(), MM()]

    def instance(self):
        self.run_manager = RunManager(hosts=self.hosts, plugins=self.plugins)

    def test_instance_without_arg(self):
        self.instance()

    def test_instance_without_arguments(self):
        self.run_manager = RunManager()
        self.assertEqual(self.run_manager.hosts, [])
        self.assertEqual(self.run_manager.plugins, [])

    def test_fetch_jobs(self):
        self.instance()
        self.assertEqual(self.run_manager.hosts, self.hosts)
        self.assertEqual(self.run_manager.plugins, self.plugins)


if __name__ == '__main__':
    unittest.main()
