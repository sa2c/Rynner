import unittest
from unittest.mock import MagicMock as MM
from rynner.behaviour import Behaviour, InvalidContextOption
from rynner.host import Host
from rynner.run import Run
from rynner.template import Template


class TestBehaviour(unittest.TestCase):
    def setUp(self):
        self.mock_conn = MM()

    def instantiate(self, opt_map=None):
        option_map = [
            ('#FAKE --walltime={}', 'walltime'),
            ('#FAKE --num-nodes={}', 'num_nodes'),
        ]
        defaults = MM()
        self.behaviour = Behaviour(option_map, defaults)
        self.connection = MM()
        self.datastore = MM()
        self.host = Host(self.behaviour, self.connection, self.datastore)

    def test_instantiation(self):
        self.instantiate()

    def test_instantiate_run(self):
        self.instantiate()
        run = Run(host=self.host, walltime='10:0:00')

    def test_instantiate_run_with_walltime(self):
        self.instantiate()
        self.host.run = MM()
        run = Run(
            host=self.host,
            walltime='10:0:00',
            num_nodes=10,
            script='this is my script')
        context = {
            'options': ['#FAKE --walltime=10:0:00', '#FAKE --num-nodes=10'],
            'script': 'this is my script'
        }
        self.host.run.assert_called_once_with(run.id, context)

    def test_instantiate_run_with_walltime(self):
        self.instantiate()
        self.host.run = MM()
        run = Run(
            host=self.host,
            walltime='10:0:00',
            num_nodes=10,
            script=Template('this is my {var}').format({
                'var': 'script'
            }))
        context = {
            'options': ['#FAKE --walltime=10:0:00', '#FAKE --num-nodes=10'],
            'script': 'this is my script'
        }
        self.host.run.assert_called_once_with(run.id, context)

    def test_throw_exception_on_invalid_option(self):
        self.instantiate()
        self.host.run = MM()
        with self.assertRaises(InvalidContextOption):
            run = Run(
                # script, uploads and downloads are "special" and are handled differently
                host=self.host,
                script='this is my script',
                walltime='10:0:00',
                num_nodes=10,
                invalid=5,
            )

    def test_upload_incorrect_formats(self):
        self.instantiate()
        self.host.run = MM()
        with self.assertRaises(InvalidContextOption):
            run = Run(host=self.host, uploads=['throw an error'])

    def test_uploads_correct_format(self):
        self.instantiate()
        self.host.run = MM()
        run = Run(host=self.host, uploads=[('local', 'remote')])
        self.connection.put_file.assert_called_once_with('local', 'remote')

    @unittest.skip("running not implemented yet")
    def test_files_run(self):
        pass

    @unittest.skip("datastore not implemented yet")
    def test_datastore(self):
        pass

    @unittest.skip("not implemented yet")
    def test_download_files(self):
        pass


if __name__ == '__main__':
    unittest.main()
