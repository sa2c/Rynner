import unittest
from unittest.mock import patch, MagicMock
from run import *


class TestRun(unittest.TestCase):
    def setUp(self):
        self.run = Run()


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
        assert self.run.options['walltime'] == walltime

    def test_walltime_minutes(self):
        walltime = 10000  # walltime in seconds
        self.run.walltime(minutes=walltime)
        assert self.run.options['walltime'] == walltime * 60

    def test_walltime_hours(self):
        walltime = 10000  # walltime in seconds
        self.run.walltime(hours=walltime)
        assert self.run.options['walltime'] == walltime * 60 * 60

    def test_walltime_compound_time(self):
        sec = 123  # walltime in seconds
        minute = 456
        hour = 789
        self.run.walltime(seconds=sec, minutes=minute, hours=hour)
        assert self.run.options[
            'walltime'] == sec + (minute * 60) + (hour * 60 * 60)

    def test_set_custom_default_options(self):
        opts = {'walltime': '12000'}
        self.run = Run(opts)
        assert self.run.options == opts

    def test_options_fail_invalid_opts(self):
        with self.assertRaises(Exception):
            self.run = Run({'invalid_options': 'invalid'})

    def test_modifying_options_raises_exception(self):
        self.run = Run()
        with self.assertRaises(Exception):
            self.run.options['invalid_option'] = 'invalid'

    def test_bandwidth_option(self):
        arg = MagicMock
        self.run.bandwidth(arg)
        assert self.run.options['bandwidth'] == arg

    def test_num_nodes_option(self):
        arg = MagicMock
        self.run.num_nodes(arg)
        assert self.run.options['num_nodes'] == arg

    def test_memory_option(self):
        arg = MagicMock
        self.run.memory(arg)
        assert self.run.options['memory'] == arg

    def test_memory_option(self):
        arg = MagicMock
        self.run.memory(kb=5, mb=10, gb=25)
        assert self.run.options[
            'memory'] == 5 + (10 * 1025) + (25 * 1025 * 1025)


class TestRunInterfaces(unittest.TestCase):
    def test_template_render_args(self):
        template = MagicMock()
        args = MagicMock()
        self.run = Run(template=template)
        self.run.from_template(args)

        template.render.assert_called_once_with(args)

    def test_jobcard_set_from_template_render_output(self):
        template = MagicMock()
        args = MagicMock()
        self.run = Run(template=template)
        self.run.from_template(args)

        assert self.run.options['jobcard'] == template.render()

    def test_jobcard_set_from_template_raises_exception_when_no_template(self):
        self.run = Run()
        args = MagicMock()
        with self.assertRaises(Exception):
            self.run.from_template(args)

    def test_from_template_takes_template_argument(self):
        self.run = Run()
        template = MagicMock()
        args = MagicMock()
        self.run = Run(template=template)
        self.run.from_template(args)

        template.render.assert_called_once_with(args)

    def test_jobcard_set_from_string_if_provided(self):
        template = MagicMock()
        string = MagicMock()
        run = Run(template=template)
        run.jobcard(string)

        assert run.options['jobcard'] == string

    def test_run_can_run(self):
        runner_inst = MagicMock()
        run = Run(runner=runner_inst)
        jobID = run.run()
        runner_inst.run.assert_called_once_with(run.options, run.downloads,
                                                run.uploads)

    def test_run_run_returns_return_value_of_runner(self):
        runner_inst = MagicMock()
        run = Run(runner=runner_inst)
        jobID = run.run()

        assert jobID == runner_inst.run()

    def test_run_errors_without_runner(self):
        run = Run()
        with self.assertRaises(RunnerNotSpecifiedException):
            run.run()


if __name__ == '__main__':
    unittest.main()
