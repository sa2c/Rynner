import unittest
from unittest.mock import MagicMock as MM
from rynner.behaviour import *


class TestBehaviour(unittest.TestCase):
    def setUp(self):
        self.mock_conn = MM()

    def instantiate(self, opt_map=None):
        self.opt_map = MM()
        if opt_map is not None:
            self.opt_map = opt_map
        self.defaults = MM()
        self.behaviour = Behaviour(self.opt_map, self.defaults)

    def assert_parse(self, opt_map, input, output):
        self.instantiate(opt_map)
        context = self.behaviour.parse(input)
        self.assertEqual(context['options'], output)
        return context

    def test_instantiation(self):
        self.instantiate()

    def test_behaviour_can_call_run(self):
        self.instantiate()
        self.behaviour.run({}, {})

    def test_behaviour_single_string_opt_map_parsed(self):
        opt_map = [
            ('#FAKE --memory={}', 'memory'),
        ]
        input = {'memory': 'MEMORY_VALUE'}
        output = [
            '#FAKE --memory=MEMORY_VALUE',
        ]

        self.assert_parse(opt_map, input, output)

    def test_behaviour_multiple_string_opt_map_parsed(self):
        opt_map = [
            ('#FAKE --memory={}', 'memory'),
            ('#FAKE --cpus={}', 'cpus'),
        ]
        input = {'memory': 'MEMORY_VALUE', 'cpus': 'CPU_VALUE'}
        output = [
            '#FAKE --memory=MEMORY_VALUE',
            '#FAKE --cpus=CPU_VALUE',
        ]

        self.assert_parse(opt_map, input, output)

    def test_behaviour_duplicate_string_matches(self):
        opt_map = [
            ('#FAKE --memory={}', 'memory'),
            ('#SHOULD SKIP ME', 'memory'),
            ('#FAKE --cpus={}', 'cpus'),
        ]
        input = {'memory': 'MEMORY_VALUE', 'cpus': 'CPU_VALUE'}
        output = [
            '#FAKE --memory=MEMORY_VALUE',
            '#FAKE --cpus=CPU_VALUE',
        ]

        self.assert_parse(opt_map, input, output)

    def test_behaviour_compound_string_matches(self):
        opt_map = [
            ('#FAKE --memory={} --cpus={}', ('memory', 'cpus')),
            ('#FAKE --memory={}', 'memory'),
            ('#FAKE --cpus={}', 'cpus'),
        ]

        input = {'memory': 'MEMORY_VALUE', 'cpus': 'CPU_VALUE'}

        output = ['#FAKE --memory=MEMORY_VALUE --cpus=CPU_VALUE']

        self.assert_parse(opt_map, input, output)

    def test_not_all_map_matched(self):
        opt_map = [
            ('#FAKE --memory={} --cpus={}', ('memory', 'cpus')),
            ('#FAKE --memory={}', 'memory'),
            ('#FAKE --cpus={}', 'cpus'),
            ('#FAKE --cpus={}', 'another_variable'),
        ]

        input = {'memory': 'MEMORY_VALUE', 'cpus': 'CPU_VALUE'}

        output = ['#FAKE --memory=MEMORY_VALUE --cpus=CPU_VALUE']

        self.assert_parse(opt_map, input, output)

    def test_error_if_unmatched_context_keys(self):
        opt_map = [
            ('#FAKE --memory={} --cpus={}', ('memory', 'cpus')),
            ('#FAKE --memory={}', 'memory'),
            ('#FAKE --cpus={}', 'cpus'),
        ]

        input = {
            'memory': 'MEMORY_VALUE',
            'cpus': 'CPU_VALUE',
            'another-var': 'ERROR!'
        }

        self.instantiate(opt_map)
        with self.assertRaises(InvalidContextOption) as context:
            context = self.behaviour.parse(input)

        assert 'invalid option(s): ' in str(context.exception)
        assert 'another-var' in str(context.exception)

    def test_reverse_argument_order(self):
        opt_map = [
            ('#FAKE --memory={} --cpus={}', ('cpus', 'memory')),
            ('#FAKE --memory={}', 'memory'),
            ('#FAKE --cpus={}', 'cpus'),
        ]

        input = {
            'memory': 'MEMORY_VALUE',
            'cpus': 'CPU_VALUE',
        }

        output = ['#FAKE --memory=CPU_VALUE --cpus=MEMORY_VALUE']

        self.assert_parse(opt_map, input, output)

    def test_input_dict_untouched(self):
        input = {'memory': 1, 'cpus': 1}
        input_copy = input.copy()
        opt_map = [
            ('#FAKE --memory={}', 'memory'),
            ('#FAKE --cpus={}', 'cpus'),
        ]
        self.instantiate(opt_map)
        self.behaviour.parse(input)
        self.assertEqual(input, input_copy)

    def test_script_returned_seperately(self):
        opt_map = [
            ('#FAKE --memory={}', 'memory'),
            ('#FAKE --cpus={}', 'cpus'),
            ('#FAKE --cpus={}', 'script'),
        ]

        input = {'memory': 'MEMORY_VALUE', 'script': 'my script'}

        output = ['#FAKE --memory=MEMORY_VALUE']

        context = self.assert_parse(opt_map, input, output)
        assert context['script'] == 'my script'

    def test_with_function(self):
        def parsing_function(a, k):
            return {'function-return': [a.copy(), k]}

        opt_map = [
            (parsing_function, ('cpus', 'memory')),
        ]

        mock_mem, mock_cpu, mock_template = (MM(), MM(), MM())

        input = {'memory': mock_mem, 'cpus': mock_cpu}

        output = [{'function-return': [input, ('cpus', 'memory')]}]

        context = self.assert_parse(opt_map, input, output)

    @unittest.skip("classes as cluster config not implemented yet")
    def test_with_class(self):
        pass


if __name__ == '__main__':
    unittest.main()
