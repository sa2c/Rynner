import unittest
from unittest.mock import MagicMock as MM, patch
from rynner.run_type import RunType, RunAction
from rynner.inputs import Interface


class TestRunType(unittest.TestCase):
    def setUp(self):
        self.runner = MM()
        self.interface = MM()
        self.data = {'a': 'a', 'b': 'b'}

        self.domain = 'rynner.swansea.ac.uk'
        self.name = 'Test Plugin'

    def instance(self):
        self.interface.data.return_value = self.data
        self.interface.invalid.return_value = []

        self.run_type = RunType(self.domain, self.name, self.interface,
                                self.runner)

    def test_instance(self):
        self.instance()

    def test_create_calls_setup(self):
        self.instance()

        self.run_type.create()
        self.runner.assert_called_once_with(self.data)

    def test_interface_show_method_called(self):
        self.instance()
        self.assertFalse(self.interface.show.called)
        self.run_type.create()
        self.assertTrue(self.interface.show.called)

    def test_can_add_action(self):
        some_action = lambda data: None

        self.instance()
        action = self.run_type.add_action('action label', some_action)
        self.assertIn(action, self.run_type.actions())

    def test_action_is_instance_of_action_class(self):
        some_action = lambda data: None

        self.instance()
        action = self.run_type.add_action('action label', some_action)
        actions = self.run_type.actions()
        self.assertIs(type(actions[0]), RunAction)

    def test_action_created_with_behaviour_and_label(self):
        self.instance()

        action_function = MM()
        action_label = MM()

        action = self.run_type.add_action(action_label, action_function)
        self.assertEqual(action.label, action_label)
        self.assertEqual(action.function, action_function)

    def test_create_can_handle_empty_data(self):
        self.instance()
        self.data = {}
        self.run_type.create()

    def test_call_runner_if_interface_valid_and_accepted(self):
        # runner is called on create when interface is valid
        self.instance()
        self.interface.show.return_value = True
        self.interface.invalid.return_value = []
        self.run_type.create()
        self.assertTrue(self.runner.called)

    def test_doesnt_call_runner_if_interface_is_invalid(self):
        # runner is not called when invalid
        self.instance()
        self.interface.show.return_value = True
        self.interface.invalid.return_value = ['a', 'b']
        self.run_type.create()
        self.assertTrue(self.interface.invalid.called)
        self.assertFalse(self.runner.called)

    def test_doesnt_call_runner_if_exec_cancelled(self):
        # runner is not called when invalid
        self.instance()
        self.interface.invalid.return_value = []
        self.interface.show.return_value = False
        self.run_type.create()
        self.assertTrue(self.interface.show.called)
        self.assertFalse(self.runner.called)

    @patch('rynner.run_type.Run')
    def test_doesnt_call_runner_default(self, MockRun):
        run_type = RunType(self.domain, self.name, self.interface)

        self.interface.invalid.return_value = []
        self.interface.show.return_value = True
        self.interface.data.return_value = {'my': 'test', 'data': 'dict'}
        run_type.create()

        MockRun.assert_called_once_with(my='test', data='dict')

    def test_set_params(self):
        params = MM()
        run_type = RunType(
            self.domain, self.name, self.interface, params=params)
        self.assertEqual(params, run_type.params)

    def test_set_params_default(self):
        run_type = RunType(self.domain, self.name, self.interface)
        self.assertEqual(run_type.params, RunType.default_params)
