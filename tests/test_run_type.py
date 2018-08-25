import unittest
from unittest.mock import MagicMock as MM, patch
from rynner.run_type import RunType, RunAction, RunTypeCollection


class TestRunType(unittest.TestCase):
    def setUp(self):
        self.runner = MM()
        self.create_view = MM()
        self.data = {'a': 'a', 'b': 'b'}

        self.domain = 'rynner.swansea.ac.uk'
        self.name = 'Test Plugin'

    def instance(self, **kwargs):
        self.create_view.data.return_value = self.data
        self.create_view.invalid.return_value = []

        self.run_type = RunType(self.domain, self.name, **kwargs)

    def test_instance(self):
        self.instance()

    def test_create_calls_setup(self):
        self.instance(runner=self.runner, create_view=self.create_view)
        self.run_type.create()
        self.runner.assert_called_once_with(self.data)

    def test_create_view_show_method_called(self):
        self.instance(create_view=self.create_view, runner=self.runner)
        self.assertFalse(self.create_view.show.called)
        self.run_type.create()
        self.assertTrue(self.create_view.show.called)

    def test_call_runner_if_no_instance(self):
        self.instance(runner=self.runner, create_view=None)
        self.run_type.create()
        self.assertFalse(self.create_view.show.called)
        self.assertTrue(self.runner.called)

    def test_can_add_action(self):
        some_action = lambda data: None

        self.instance()
        action = self.run_type.add_action('action label', some_action)
        self.assertIn(action, self.run_type.actions)

    def test_action_is_instance_of_action_class(self):
        some_action = lambda data: None

        self.instance()
        action = self.run_type.add_action('action label', some_action)
        actions = self.run_type.actions
        self.assertIs(type(actions[0]), RunAction)

    def test_action_created_with_behaviour_and_label(self):
        self.instance()

        action_function = MM()
        action_label = MM()

        action = self.run_type.add_action(action_label, action_function)
        self.assertEqual(action.label, action_label)
        self.assertEqual(action.function, action_function)

    def test_create_can_handle_empty_data(self):
        self.instance(runner=self.runner)
        self.data = {}
        self.run_type.create()

    def test_call_runner_if_create_view_valid_and_accepted(self):
        # runner is called on create when create_view is valid
        self.instance(runner=self.runner)
        self.create_view.show.return_value = True
        self.create_view.invalid.return_value = []
        self.run_type.create()
        self.assertTrue(self.runner.called)

    def test_doesnt_call_runner_if_create_view_is_invalid(self):
        # runner is not called when invalid
        self.instance(runner=self.runner, create_view=self.create_view)
        self.create_view.show.return_value = True
        self.create_view.invalid.return_value = ['a', 'b']
        self.run_type.create()
        self.assertTrue(self.create_view.invalid.called)
        self.assertFalse(self.runner.called)

    def test_doesnt_call_runner_if_exec_cancelled(self):
        # runner is not called when invalid
        self.instance(runner=self.runner, create_view=self.create_view)
        self.create_view.invalid.return_value = []
        self.create_view.show.return_value = False
        self.run_type.create()
        self.assertTrue(self.create_view.show.called)
        self.assertFalse(self.runner.called)

    @patch('rynner.run_type.Run')
    def test_doesnt_call_runner_default(self, MockRun):
        run_type = RunType(self.domain, self.name, self.create_view)

        self.create_view.invalid.return_value = []
        self.create_view.show.return_value = True
        self.create_view.data.return_value = {'my': 'test', 'data': 'dict'}
        run_type.create()

        MockRun.assert_called_once_with(my='test', data='dict')

    def test_set_view_keys_stored(self):
        view_keys = MM()
        run_type = RunType(
            self.domain, self.name, self.create_view, view_keys=view_keys)
        self.assertEqual(view_keys, run_type.view_keys)

    def test_set_view_keys_default(self):
        run_type = RunType(self.domain, self.name, self.create_view)
        self.assertEqual(run_type.view_keys, RunType.view_keys)

    def test_assert_default_view_keys_values(self):
        self.assertEqual(RunType.view_keys, (
            "id",
            "name",
        ))

    def test_default_param_values(self):
        run_type = RunType(self.domain, self.name, self.create_view)
        self.assertEqual(run_type.view_keys, ("id", "name"))

    def test_add_list_jobs(self):
        self.instance()
        ret = self.run_type.list_jobs([])
        self.assertEqual(ret, [])

    def test_add_list_jobs(self):
        self.instance()
        host1 = MM()
        host1.jobs.return_value = ['host1-job1', 'host1-job2']
        ret = self.run_type.list_jobs([host1])
        self.assertEqual(ret, ['host1-job1', 'host1-job2'])

    def test_add_list_jobs_multi_hosts(self):
        self.instance()
        host1 = MM()
        host1.jobs.return_value = ['host1-job1', 'host1-job2']
        host2 = MM()
        host2.jobs.return_value = ['host2-job2', 'host2-job2']
        ret = self.run_type.list_jobs([host1, host2])
        self.assertEqual(
            ret, ['host1-job1', 'host1-job2', 'host2-job2', 'host2-job2'])

    def test_calls_host_jobs_with_domain(self):
        self.instance()
        host = MM()
        self.run_type.list_jobs([host])
        host.jobs.assert_called_once_with(self.domain)

    def test_add_labels(self):
        labels = MM()
        run_type = RunType(self.domain, self.name, labels=labels)
        self.assertEqual(run_type.labels, labels)

    def test_add_labels(self):
        labels = MM()
        run_type = RunType(self.domain, self.name)
        self.assertEqual(run_type.labels, None)

    def test_build_index_view(self):
        view_class = MM()
        self.instance(build_index_view=view_class)
        self.assertEqual(self.run_type.build_index_view, view_class)

    def test_build_index_view_default(self):
        self.instance()
        self.assertEqual(self.run_type.build_index_view, None)

    def test_create_view_is_stored(self):
        create_view = MM()
        self.instance(create_view=create_view)
        self.assertEqual(self.run_type.create_view, create_view)

    def test_create_view_none_by_default(self):
        self.instance()
        self.assertEqual(self.run_type.create_view, None)


class TestRunTypeCollection(unittest.TestCase):
    def setUp(self):
        self.name = 'Test Collection Name'
        self.run_types = [MM(), MM()]

    def instance(self, **kwargs):
        self.rc = RunTypeCollection(self.name, self.run_types, **kwargs)

    def test_instance(self):
        self.instance()

    def test_has_name_attr(self):
        self.instance()
        self.assertEqual(self.rc.name, self.name)

    def test_has_run_types(self):
        self.instance()
        self.assertEqual(self.rc.run_types, self.run_types)

    def test_has_view_keys_with_default(self):
        self.instance()
        self.assertEqual(self.rc.view_keys, RunType.view_keys)

    def test_has_view_keys_as_specified(self):
        view_keys = MM()
        self.instance(view_keys=view_keys)
        self.assertEqual(self.rc.view_keys, view_keys)

    def test_add_labels(self):
        labels = MM()
        run_type = RunTypeCollection(self.name, self.run_types, labels=labels)
        self.assertEqual(run_type.labels, labels)

    def test_labels_none_by_default(self):
        run_type = RunTypeCollection(self.name, self.run_types)
        self.assertEqual(run_type.labels, None)

    def test_create_view_none_by_default(self):
        self.instance()
        self.assertEqual(self.rc.create_view, None)

    def test_has_build_index_view_none(self):
        self.instance()
        self.assertEqual(self.rc.build_index_view, None)

    def test_list_jobs(self):
        self.instance()

        # build hosts
        host1 = MM()
        host1.jobs.return_value = ['host1-job1', 'host1-job2']
        host2 = MM()
        host2.jobs.return_value = ['host2-job2', 'host2-job2']
        hosts = [host1, host2]

        # list hosts
        ret = self.rc.list_jobs(hosts)

        # list repeated twice (once for each RunType)
        # with all host1 first and host2 second
        jobs = [
            'host1-job1', 'host1-job2', 'host1-job1', 'host1-job2',
            'host2-job2', 'host2-job2', 'host2-job2', 'host2-job2'
        ]

        # check calls to host.jobs
        self.assertEqual(ret, jobs)

        # check for host1
        for host in [host1, host2]:
            call_arg_list = host.jobs.call_args_list
            call_type1, call_type2 = call_arg_list

            args, vals = call_type1
            self.assertEqual(args, (self.run_types[0].domain, ))

            args, vals = call_type2
            self.assertEqual(args, (self.run_types[1].domain, ))
