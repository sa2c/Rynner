import unittest
from unittest.mock import MagicMock as MM
from rynner.run_manager import RunManager


class TestRunManager(unittest.TestCase):
    def setUp(self):
        self.hosts = [MM(), MM()]
        self.run_types = [MM(), MM()]

    def instance(self):
        self.run_manager = RunManager(
            hosts=self.hosts, run_types=self.run_types)

    def test_instance_without_arg(self):
        self.instance()

    def test_instance_without_arguments(self):
        self.run_manager = RunManager()
        self.assertEqual(self.run_manager.hosts, [])
        self.assertEqual(self.run_manager.run_types, [])

    def test_fetch_jobs(self):
        self.instance()
        self.assertEqual(self.run_manager.hosts, self.hosts)
        self.assertEqual(self.run_manager.run_types, self.run_types)


if __name__ == '__main__':
    unittest.main()
