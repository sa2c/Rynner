import unittest
from unittest.mock import MagicMock as MM
from rynner.run_type import RunType, RunAction


class TestRunType(unittest.TestCase):
    def setUp(self):
        self.runner = MM()
        self.interface = MM()
        self.data = {'a': 'a', 'b': 'b'}

    def instance(self):
        self.interface.data.return_value = self.data

        self.run_type = RunType(self.runner, self.interface)

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
        self.assertTrue(self.interface. exec .called)

    def test_can_add_action(self):
        def an_action(data):
            pass

        self.instance()
        action = self.run_type.add_action('action label', an_action)
        self.assertIn(action, self.run_type.actions())

    def test_action_is_instance_of_action_class(self):
        def an_action(data):
            pass

        self.instance()
        action = self.run_type.add_action('action label', an_action)
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
        self.interface.valid.return_value = True
        self.interface. exec .return_value = True
        self.instance()
        self.run_type.create()
        self.assertTrue(self.runner.called)

    def test_doesnt_call_runner_if_interface_is_invalid(self):
        # runner is not called when invalid
        self.interface.valid.return_value = False
        self.interface. exec .return_value = True
        self.instance()
        self.run_type.create()
        self.assertTrue(self.interface.valid.called)
        self.assertFalse(self.runner.called)

    def test_doesnt_call_runner_if_exec_is_invalid(self):
        # runner is not called when invalid
        self.interface.valid.return_value = True
        self.interface. exec .return_value = False
        self.instance()
        self.run_type.create()
        self.assertTrue(self.interface. exec .called)
        self.assertFalse(self.runner.called)
