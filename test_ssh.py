import unittest
from unittest.mock import patch
from ssh import SSHAdapter


class TestSSH(unittest.TestCase):
    def setUp(self):
        self.cluster_host = 'example.cluster.com'
        self.cluster_user = 'user'

        self.patcher = patch('ssh.Connection')
        self.ConnMock = self.patcher.start()

        self.ssh = SSHAdapter()
        self.ssh.connect(host=self.cluster_host, user=self.cluster_user)

    def tearDown(self):
        self.patcher.stop()

    def test_connection(self):
        pass

    def test_run_command_ls(self):
        self.ssh.run_command("ls")

    def test_run_command_creates_connection(self):
        self.ssh.run_command("ls")
        assert self.ConnMock.called_once_with(
            host=self.cluster_host, user=self.cluster_user)

    def test_run_command_calls_run(self):
        cmd = "ls"
        self.ssh.run_command(cmd)
        self.ConnMock().run.assert_called_once_with(cmd)

    def test_run_command_calls_sets_dir(self):
        cmd = "ls"
        pwd = "/some/working/dir"
        self.ssh.run_command(cmd, pwd=pwd)
        self.ConnMock().cd.assert_called_once_with(pwd)

    def test_call_put_file(self):
        self.ssh.put_file("some/local/file", "/some/remote/file")

    def test_put_uploads_file(self):
        local = "/some/local/file"
        remote = "/some/remote/file"
        self.ssh.put_file(local, remote)
        self.ConnMock().put_file.called_once_with(local, remote)

    def test_call_get_file(self):
        local = "/some/local/file"
        remote = "/some/remote/file"
        self.ssh.get_file(remote, local)

    def test_file_downloads_file(self):
        remote = "/some/remote/file"
        local = "some/local/path"
        self.ssh.get_file(remote, local)
        assert self.ConnMock().get().called_once_with(remote, local)


if __name__ == '__main__':
    unittest.main()
