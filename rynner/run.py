import collections
import uuid


class RunManager:
    allowed_types = [int, str]
    key_filter = ['host', 'uploads']

    def __init__(self, plugin_id, config_options):
        '''
        Parameters
        ----------
        `plugin_id`: str
           A string giving a globally unique name for the plugin. Clients on
           different machines will use this name to associate jobs with a given
           Plugin class. The recommended appraoach is to use a web URL (such as
           a github repository URL) which is unique for this plugin. This
           string is never displayed in the UI by default (see :func:`Plugin.__init__ method <rynner.plugin.Plugin.__init__>`).

        `config_options` :
 

        '''
        self.plugin_id = plugin_id
        self.config_options = config_options
        self.datastore = {}
        self._userdata = {}

    def userdata(self, userdata):
        '''
        Utility method for storing data (a dictionary) in a datastore
        (another dictionary) which will be automatically be made
        available to actions after the run has completed.

        Parameters
        ----------
        `userdata`: dict,collections.Mapping
            The data to be stored.

        '''
        if not isinstance(userdata, collections.Mapping):
            raise ValueError('arguments to store method should be a dict')
        self._userdata.update(userdata)

    def new(self, **options):
        '''This should be called by plugin developers to create or run a new job.

        '''
        run_id = str(uuid.uuid1())

        data = options.copy()

        if 'host' not in options.keys():
            raise HostNotSpecifiedException(
                'No hosts have been specified for this run')

        # Alternative filter for multiple types
        host_dict = {
            k: self.__convert(data[k])
            for k in data.keys() if k not in self.key_filter
        }

        if not hasattr(options['host'], 'parse'):
            raise InvalidHostSpecifiedException(
                'The object specified by host key should have a parse method')

        context = options['host'].parse(self.plugin_id, run_id, host_dict)

        if 'uploads' in data.keys():
            options['host'].upload(self.plugin_id, run_id, data['uploads'])

        exit_status = options['host'].run(self.plugin_id, run_id, context)

        # store hashable options for writing to remote filesystem later
        store = {
            'plugin-identifier': self.plugin_id,
            'run-options': options.copy(),
            'framework': {
                'submit-exit-status': exit_status,
            },
        }

        self.datastore[run_id] = store

        return run_id

    def store(self):
        '''Store data about the runs contained in this RunManager.

        This method is called by the Rynner framework to initialise storing of
        data, it should not be called explicitly by a plugin developer.

        '''
        for run_id, data in self.datastore.items():
            host = data['run-options'].pop('host')
            data.update({
                'config-options': self.config_options,
                'userdata': self._userdata
            })
            host.store(self.plugin_id, run_id, data)

    def __convert(self, value):
        if type(value) in self.allowed_types:
            return value
        else:
            try:
                return value.__rynner_value__()
            except:
                raise UnconvertableOptionType(
                    'no __rynner_value__ method on {}'.format(value))


class UnconvertableOptionType(AttributeError):
    pass


class HostNotSpecifiedException(AttributeError):
    pass


class InvalidHostSpecifiedException(AttributeError):
    pass
