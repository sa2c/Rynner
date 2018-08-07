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


class TestRunFileTransfers(TestRun):
    def test_instansiation(self):
        assert isinstance(self.run, Run)

    def test_notifies_download(self):
        ''' stores a single download '''
        local = MagicMock()
        remote = MagicMock()
        self.run.download(local=local, remote=remote)
        self.mock_runner.download.assert_called_once_with(
            self.rcontext, remote, local)

    def test_notifies_download_with_arguments(self):
        ''' stores a single download '''
        local = MagicMock()
        remote = MagicMock()
        self.run.download(local=local, remote=remote, some_keyword='a')
        self.mock_runner.download.assert_called_once_with(
            self.rcontext, remote, local, some_keyword='a')

    def test_notifies_upload(self):
        ''' stores a single upload '''
        local = MagicMock()
        remote = MagicMock()
        self.run.upload(local=local, remote=remote)
        self.mock_runner.upload.assert_called_once_with(
            self.rcontext, local, remote)

    def test_notifies_upload_with_arguments(self):
        ''' stores a single upload '''
        local = MagicMock()
        remote = MagicMock()
        self.run.upload(local=local, remote=remote, some_keyword='a')
        self.mock_runner.upload.assert_called_once_with(
            self.rcontext, local, remote, some_keyword='a')


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

    def test_num_cores_option(self):
        arg = MagicMock
        self.run.num_cores(arg)
        self.mock_runner.behaviour.num_cores.assert_called_once_with(
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
        run = Run(self.mock_data, host=self.mock_runner)
        jobID = run.run()
        self.mock_runner.run.assert_called_once_with(self.rcontext,
                                                     self.bcontext)

    def test_run_run_returns_return_value_of_runner(self):
        run = Run(self.mock_data, host=self.mock_runner)
        jobID = run.run()

        assert jobID == self.mock_runner.run()

    def test_run_errors_without_runner(self):
        with self.assertRaises(HostNotSpecifiedException):
            run = Run(self.mock_data)

    def test_stores_data_in_datastore(self):
        assert self.run.data == self.mock_data


if __name__ == '__main__':
    unittest.main()
