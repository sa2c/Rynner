import unittest
from unittest.mock import patch, call, ANY
from unittest.mock import MagicMock as MM
from rynner.host import *


class TestConnection(unittest.TestCase):
    def setUp(self):
        self.cluster_host = 'example.cluster.com'
        self.cluster_user = 'user'
        self.context = MM()

        self.patcher = patch('rynner.host.fabric.Connection')
        self.FabricMock = self.patcher.start()

        self.connection = Connection(
            host=self.cluster_host, user=self.cluster_user)

    def tearDown(self):
        self.patcher.stop()

    def test_connection(self):
        pass

    def test_run_command_ls(self):
        self.connection.run_command("ls")

    def test_run_command_creates_connection(self):
        self.connection.run_command("ls")
        self.FabricMock.assert_called_once_with(
            host=self.cluster_host, user=self.cluster_user)

    def test_run_command_calls_run(self):
        cmd = "ls"
        self.connection.run_command(cmd)
        self.FabricMock().run.assert_called_once_with(cmd)

    def test_run_command_calls_sets_dir(self):
        cmd = "ls"
        pwd = "/some/working/dir"
        self.connection.run_command(cmd, pwd=pwd)
        self.FabricMock().cd.assert_called_once_with(pwd)

    def test_put_uploads_file(self):
        local = "/some/local/file"
        remote = "/some/remote/file"
        self.connection.put_file(local, remote)
        self.FabricMock().put.assert_called_once_with(local, remote)

    def test_call_get_file(self):
        local = "/some/local/file"
        remote = "/some/remote/file"
        self.connection.get_file(remote, local)

    def test_file_downloads_file(self):
        remote = "/some/remote/file"
        local = "some/local/path"
        self.connection.get_file(remote, local)
        self.FabricMock().get.assert_called_once_with(remote, local)

    def test_put_content(self):
        self.connection.put_file_content('/my/remote/path', 'content')

        # get method that is called
        callee = self.FabricMock().put

        # method only called once
        callee.assert_called_once()

        # check arguments
        call_args_list = callee.call_args_list
        args, kwargs = call_args_list[0]
        content, remote_path = args
        content = content.getvalue()
        self.assertEqual(content, 'content')
        self.assertEqual(remote_path, '/my/remote/path')


class TestHost(unittest.TestCase):
    def setUp(self):
        self.conn_patch = patch('rynner.host.Connection')
        MockConnection = self.conn_patch.start()
        self.mock_connection = MockConnection()

    def tearDown(self):
        self.conn_patch.stop()

    def instantiate(self):
        # instantiate Host
        self.mock_behaviour = MM()
        self.mock_connection = MM()
        self.mock_datastore = MM()
        self.host = Host(self.mock_behaviour, self.mock_connection,
                         self.mock_datastore)

        self.context = MM()

    def test_instantiation(self):
        self.instantiate()

    def test_file_upload_single_tuple(self):
        self.instantiate()

        local = MM()
        remote = MM()
        uploads = ((local, remote), )
        self.host.upload(self.id, uploads)
        self.mock_connection.put_file.assert_called_once_with(local, remote)

    def test_file_exception_invalid_tuple_length(self):
        self.instantiate()

        local = MM()
        remote = MM()
        uploads = (local, remote, local)
        with self.assertRaises(InvalidContextOption) as context:
            self.host.upload(self.id, uploads)
        assert 'invalid format for uploads options' in str(context.exception)

    def test_file_upload_single_list(self):
        self.instantiate()

        local = MM()
        remote = MM()
        uploads = [(local, remote)]
        self.host.upload(self.id, uploads)
        self.mock_connection.put_file.assert_called_once_with(local, remote)

    def test_file_upload_multiple_list(self):
        self.instantiate()

        local = MM()
        remote = MM()
        local2 = MM()
        remote2 = MM()
        uploads = [(local, remote), (local2, remote2)]
        self.host.upload(self.id, uploads)
        calls = [call.put_file(local, remote), call.put_file(local2, remote2)]
        self.mock_connection.assert_has_calls(calls)

    def test_parse_creates_dict_context(self):
        self.instantiate()

        dict = {}
        context = self.host.parse(MM(), dict)

    def test_parse_handled_by_behaviour_method(self):
        self.instantiate()
        options = MM()
        self.host.parse(MM(), options)
        self.mock_behaviour.parse.assert_called_once_with(options)

    def test_parse_returns_context_from_behaviour(self):
        self.instantiate()
        context = self.host.parse(MM(), MM())
        assert context == self.mock_behaviour.parse()

    def test_run_handled_by_behaviour_method(self):
        self.instantiate()
        context = MM()
        self.host.run(1536, context)
        self.mock_behaviour.run.assert_called_once_with(ANY, context, '1536')

    def test_type_handled_by_behaviour(self):
        self.instantiate()
        string = MM()
        self.host.type(string)
        self.mock_behaviour.type.assert_called_once_with(string)

    def test_returns_value_of_behaviour(self):
        self.instantiate()
        ret = self.host.type(MM())
        assert ret == self.mock_behaviour.type()

    def test_run_passes_connection(self):
        self.instantiate()
        options = MM()
        id = '9843759'
        self.host.run(id, options)
        self.mock_behaviour.run.assert_called_once_with(
            self.mock_connection, options, id)

    def test_stores_options_in_datastore(self):
        self.instantiate()
        options = MM()
        id = MM()
        self.host.parse(id, options)
        self.mock_datastore.store.assert_called_once_with(id, options)

    def test_stores_runstate(self):
        self.instantiate()
        context = MM()
        id = MM()
        self.host.run(id, context)
        self.mock_datastore.isrunning.assert_called_once_with(
            id, self.mock_behaviour.run())

    def test_jobs_returns_jobs_from_datastore(self):
        self.instantiate()
        run_type = MM()
        self.assertFalse(self.mock_datastore.jobs.called)
        self.host.jobs(run_type)
        self.mock_datastore.jobs.assert_called_once_with(type=run_type)

    def test_jobs_calls_datastore_with_none_by_default(self):
        self.instantiate()
        self.assertFalse(self.mock_datastore.jobs.called)
        self.host.jobs()
        self.mock_datastore.jobs.assert_called_once_with(type=None)

    def test_jobs_returns_datastore_result(self):
        self.instantiate()
        ret = self.host.jobs()
        self.assertEqual(ret, self.mock_datastore.jobs())


if __name__ == '__main__':
    unittest.main()
