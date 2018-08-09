import uuid


class Run:
    allowed_types = [int, str]
    key_filter = ['host', 'uploads']

    def __init__(self, **options):
        self.id = uuid.uuid1().int

        data = options.copy()

        if 'host' not in options.keys():
            raise HostNotSpecifiedException

        # Alternative filter for multiple types
        host_dict = {
            k: self.__convert(data[k])
            for k in data.keys() if k not in self.key_filter
        }

        context = options['host'].parse(host_dict)

        # TODO uploads should be handled in the run method of the host rather than in the run?
        if 'uploads' in data.keys():
            options['host'].upload(self.id, data['uploads'])

        # this has changed, should also pass id
        options['host'].run(self.id, context)


#       TODO - queue downloads on the host for instance finishing - and store by jobID
#       self.host.queue_downloads(self.runid, self.downloads)

#       TODO - implement sync, can this be done in actions instead?
#       self.host.sync(self.runid, self.downloads)

    def __convert(self, value):
        if type(value) in self.allowed_types:
            return value
        else:
            try:
                return value.__rynner_value__()
            except:
                raise UnconvertableOptionType(
                    f'no __rynner_value__ method on {value}')


class UnconvertableOptionType(AttributeError):
    pass


class HostNotSpecifiedException(AttributeError):
    pass
