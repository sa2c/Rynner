import unittest
from unittest.mock import MagicMock
from runner import *


class TestRunner(unittest.TestCase):
    def setUp(self):
        self.args = [MagicMock(), MagicMock(), MagicMock(), MagicMock()]
        self.mock_logic = MagicMock()
        self.runner = Runner(self.mock_logic)

    def test_runner_instantiate(self):
        assert isinstance(self.runner, Runner)

    def test_runner_is(self):
        assert self.runner.type(Runner) == True

    def test_runner_isnt(self):
        class Runt:
            pass

        assert self.runner.type(Runt) == False

    def test_can_call_run(self):
        self.runner.run(*self.args)

    def test_run_call_invalid_without_arguments(self):
        with self.assertRaises(TypeError) as context:
            self.runner.run()

        assert 'missing 4 required positional arguments' in str(
            context.exception)
