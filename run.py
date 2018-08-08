import uuid


class Run:
    allowed_types = [int, str]
    key_filter = ['host', 'uploads']

    def __init__(self, options):
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

        if 'uploads' in data.keys():
            options['host'].upload(self.id, data['uploads'])

        options['host'].run(context)


#       TODO - queue downloads on the host for instance finishing - and store by jobID
#       self.host.queue_downloads(self.runid, self.downloads)

#       TODO - implement sync, can this be done in actions instead?
#       self.host.sync(self.runid, self.downloads)

    def __convert(self, value):
        if type(value) in self.allowed_types:
            return value
        else:
            return value.__rynner_value__()


class HostNotSpecifiedException(AttributeError):
    pass
