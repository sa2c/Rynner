import unittest
from unittest.mock import patch, MagicMock
from run import *


class TestRun(unittest.TestCase):
    def setUp(self):
        self.mock_data = MagicMock()
        self.mock_runner = MagicMock()
        self.run = Run(self.mock_data, self.mock_runner)

        self.bcontext = self.mock_runner.behaviour.get_context()
        self.rcontext = self.mock_runner.get_context()


class TestRunDownload(TestRun):
    def test_instansiation(self):
        assert isinstance(self.run, Run)

    def test_downloads_empty_initially(self):
        assert self.run.downloads == []

    def test_stores_single_download(self):
        ''' stores a single download '''
        self.run.download(local='local1', remote='remote1')
        assert self.run.downloads[0] == ('local1', 'remote1')
        assert len(self.run.downloads) == 1

    def test_stores_single_download_without_keywords(self):
        ''' stores a single download '''
        self.run.download('remote1', 'local1')
        assert self.run.downloads[0] == ('local1', 'remote1')
        assert len(self.run.downloads) == 1

    def test_stores_multiple_downloads(self):
        ''' stores a single download '''
        local = ('local1', 'local2')
        remote = ('remote1', 'remote2')
        self.run.download(local=local, remote=remote)
        assert self.run.downloads == list(zip(local, remote))
        assert len(self.run.downloads) == 2

    def test_stores_downloads_with_interval(self):
        ''' stores a single download with interval '''
        self.run.download(local='local1', remote='remote1', interval=3)
        assert self.run.downloads == [('local1', 'remote1', {'interval': 3})]
        assert len(self.run.downloads) == 1

    def test_stores_downloads_with_interval_on_one_file(self):
        ''' stores a single download with interval and single download with no interval'''
        self.run.download(local='local1', remote='remote1')
        self.run.download(local='local2', remote='remote2', interval=3)
        assert self.run.downloads == [('local1', 'remote1'), ('local2',
                                                              'remote2', {
                                                                  'interval': 3
                                                              })]
        assert len(self.run.downloads) == 2

    def test_stores_downloads_filters_keywords(self):
        with self.assertRaises(InvalidDownloadOptionException):
            self.run.download(local='local2', remote='remote2', some_keyword=3)


class TestRunUploads(TestRun):
    def test_instansiation(self):
        assert isinstance(self.run, Run)

    def test_downloads_empty_initially(self):
        assert self.run.uploads == []

    def test_stores_single_download(self):
        ''' stores a single download '''
        self.run.upload(local='local1', remote='remote1')
        assert self.run.uploads[0] == ('local1', 'remote1')
        assert len(self.run.uploads) == 1

    def test_stores_multiple_uploads(self):
        ''' stores a single upload '''
        local = ('local1', 'local2')
        remote = ('remote1', 'remote2')
        self.run.upload(local=local, remote=remote)
        assert self.run.uploads == list(zip(local, remote))
        assert len(self.run.uploads) == 2

    def test_stores_uploads_doesnt_accept_interval(self):
        ''' stores a single upload with interval '''
        with self.assertRaises(InvalidUploadOptionException):
            self.run.upload(local='local1', remote='remote1', interval=3)

        # assert upload not added
        assert self.run.uploads == []

    def test_stores_multiple_uploads(self):
        ''' stores a single upload with interval and single upload with no interval'''
        self.run.upload(local='local1', remote='remote1')
        self.run.upload(local='local2', remote='remote2')
        assert self.run.uploads == [('local1', 'remote1'), ('local2',
                                                            'remote2')]
        assert len(self.run.uploads) == 2

    def test_stores_uploads_filters_keywords(self):
        with self.assertRaises(InvalidUploadOptionException):
            self.run.upload(
                local='local2', remote='remote2', some_keyword='test')


class TestRunOptions(TestRun):
    def test_walltime_adds_to_options(self):
        walltime = 10000  # walltime in seconds
        self.run.walltime(walltime)
        self.mock_runner.behaviour.walltime.assert_called_once_with(
            self.bcontext, walltime)

    def test_walltime_minutes(self):
        walltime = 10000  # walltime in seconds
        self.run.walltime(minutes=walltime)
        self.mock_runner.behaviour.walltime.assert_called_once_with(
            self.bcontext, walltime * 60)

    def test_walltime_hours(self):
        walltime = 10000  # walltime in seconds
        self.run.walltime(hours=walltime)
        self.mock_runner.behaviour.walltime.assert_called_once_with(
            self.bcontext, walltime * 60 * 60)

    def test_walltime_compound_time(self):
        sec = 123  # walltime in seconds
        minute = 456
        hour = 789
        self.run.walltime(seconds=sec, minutes=minute, hours=hour)
        self.mock_runner.behaviour.walltime.assert_called_once_with(
            self.bcontext, sec + (minute * 60) + (hour * 60 * 60))

    def test_set_custom_default_options(self):
        walltime = 1234
        self.run = Run(
            self.mock_data,
            self.mock_runner,
            options={
                'walltime': walltime,
                'memory': 10
            })
        self.mock_runner.behaviour.walltime.assert_called_once_with(
            self.bcontext, walltime)
        self.mock_runner.behaviour.memory.assert_called_once_with(
            self.bcontext, 1024 * 10)

    def test_options_fail_invalid_opts(self):
        with self.assertRaises(Exception):
            self.run = Run(self.mock_data, options,
                           {'invalid_options': 'invalid'})

    def test_modifying_options_raises_exception(self):
        self.run = Run(self.mock_data, self.mock_runner)
        with self.assertRaises(Exception):
            self.run.options['invalid_option'] = 'invalid'

    def test_bandwidth_option(self):
        arg = MagicMock
        self.run.bandwidth(arg)
        self.mock_runner.bandwidth.assert_called_once_with(self.rcontext, arg)

    def test_num_nodes_option(self):
        arg = MagicMock
        self.run.num_nodes(arg)
        self.mock_runner.behaviour.num_nodes.assert_called_once_with(
            self.bcontext, arg)

    def test_memory_option(self):
        arg = MagicMock
        self.run.memory(arg)
        self.mock_runner.behaviour.memory.assert_called_once_with(arg)

    def test_memory_option(self):
        arg = MagicMock
        self.run.memory(kb=5, mb=10, gb=25)
        self.mock_runner.behaviour.memory.assert_called_once_with(
            self.bcontext, 5 + (10 * 1024) + (25 * 1024 * 1024))


class TestRunInterfaces(TestRun):
    def test_template_render_args(self):
        template = MagicMock()
        args = MagicMock()
        self.run = Run(self.mock_data, self.mock_runner, template=template)
        self.run.from_template(args)

        template.render.assert_called_once_with(args)

    def test_script_set_from_template_render_output(self):
        template = MagicMock()
        args = MagicMock()
        self.run = Run(self.mock_data, self.mock_runner, template=template)
        self.run.from_template(args)

        self.mock_runner.behaviour.script.assert_called_once_with(
            self.bcontext, template.render())

    def test_script_set_from_template_raises_exception_when_no_template(self):
        self.run = Run(self.mock_data, self.mock_runner)
        args = MagicMock()
        with self.assertRaises(Exception):
            self.run.from_template(args)

    def test_from_template_takes_template_argument(self):
        self.run = Run(self.mock_data, self.mock_runner)
        template = MagicMock()
        args = MagicMock()
        self.run = Run(self.mock_data, self.mock_runner, template=template)
        self.run.from_template(args)

        template.render.assert_called_once_with(args)

    def test_script_set_from_string_if_provided(self):
        template = MagicMock()
        string = MagicMock()
        run = Run(self.mock_data, self.mock_runner, template=template)
        run.script(string)

        self.mock_runner.behaviour.script.assert_called_once_with(
            self.bcontext, string)

    def test_run_can_run(self):
        run = Run(self.mock_data, runner=self.mock_runner)
        jobID = run.run()
        self.mock_runner.run.assert_called_once_with(self.rcontext,
                                                     self.bcontext)

    def test_run_run_returns_return_value_of_runner(self):
        run = Run(self.mock_data, runner=self.mock_runner)
        jobID = run.run()

        assert jobID == self.mock_runner.run()

    def test_run_errors_without_runner(self):
        with self.assertRaises(RunnerNotSpecifiedException):
            run = Run(self.mock_data)

    def test_stores_data_in_datastore(self):
        assert self.run.data == self.mock_data


if __name__ == '__main__':
    unittest.main()
