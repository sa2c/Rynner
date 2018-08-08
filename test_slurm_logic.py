import slurm_logic
import uuid
from unittest.mock import MagicMock, call
import unittest


class TestSlurmAdapterSubmit(unittest.TestCase):
    def setUp(self):
        self.mock_ssh = MagicMock()
        self.mock_jobcard = MagicMock()
        self.mock_options = MagicMock()
        self.mock_uuid = MagicMock()
        self.mock_dir = MagicMock()

    # def submit(self):
    def submit(self):
        slurm_logic.submit(self.mock_dir, self.mock_sched_options,
                           self.mock_ssh)

    def test_takes_correct_arguments(self):
        self.submit()

    def test_creates_directory_from_mock_uuid(self):
        self.submit()
        self.mock_ssh.create_directory.assert_called_once_with(self.mock_dir)

        ### EEEEK!!
    def test_places_jobcard_in_basedir(self):
        self.submit()
        self.mock_ssh.put_file_contents.assert_called_once_with(
            f'{str(self.uuid)}/jobcard', self.mock_jobcard)

    def test_places_jobcard_after_creating_basedir(self):
        self.submit()
        calls = [
            call.create_directory(unittest.mock.ANY),
            call.put_file_contents(unittest.mock.ANY, self.mock_jobcard)
        ]
        self.mock_ssh.assert_has_calls(calls)

    def test_upload_files_to_relative_paths(self):
        self.submit()
        calls = call.put_file('local', 'remote'), call.put_file(
            'local2', 'remote2')
        self.mock_ssh.assert_has_calls(calls)
