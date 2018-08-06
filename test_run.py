from unittest.mock import MagicMock
import unittest
from unittest.mock import patch
from runnable import *


class TestRun(unittest.TestCase):
    def setUp(self):
        self.run = Run()
        #self.patcher = patch('runnable.SSHAdapter')
        #self.ConnMock = self.patcher.start()


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
    def test_default_options_empty(self):
        assert self.run.options == {}

    def test_set_custom_default_options(self):
        opts = {'walltime': '12000'}
        self.run = Run(opts)
        assert self.run.options == opts

    def test_custom_default_options_not_iterable(self):
        with self.assertRaises(TypeError) as context:
            self.run = Run(1)

        assert 'options argument should be a dict' in str(context.exception)

    def test_walltime_adds_to_options(self):
        walltime = 10000  # walltime in seconds
        self.run.walltime(walltime)
        assert self.run.options['walltime'] == walltime

    def test_invalid_options_not_added_on_create(self):
        with self.assertRaises(InvalidOptionException) as context:
            self.run = Run({'invalid_option': 'invalid'})

        assert 'invalid_option' in str(context.exception)

    def test_cannot_add_to_named_tuple(self):
        pass


if __name__ == '__main__':
    unittest.main()
