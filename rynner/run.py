import uuid


class RunManager:
    '''
    This object is created by a 'setup' function, or 'runner'
    (see design.org example)
    '''
    allowed_types = [int, str]
    key_filter = ['host', 'uploads']

    def __init__(self, plugin_id):
        self.plugin_id = plugin_id

    def new(self, **options):
        self.id = str(uuid.uuid1())

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

        context = options['host'].parse(self.plugin_id, self.id, host_dict)

        if 'uploads' in data.keys():
            options['host'].upload(self.plugin_id, self.id, data['uploads'])

        options['host'].run(self.plugin_id, self.id, context)

        return self.id

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
