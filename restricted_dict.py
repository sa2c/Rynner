import collections


class RestrictedDictException(KeyError):
    pass


class InvalidOptionException(RestrictedDictException):
    pass


class InvalidDictSpecException(RestrictedDictException):
    pass


class RestrictedDict(dict):

    __allowed = set()

    def __init__(self, options=None, allowed=None):

        if allowed is not None:
            # check that options is a dict
            if not isinstance(allowed, collections.Iterable):
                raise InvalidDictSpecException(
                    f'allowed should be iterable: {allowed}')

            self.__allowed = allowed

        if options is not None:
            # check that options is a dict
            if not isinstance(options, dict):
                raise InvalidDictSpecException(
                    f'options should be a dict: {options}')

            # iterate over options to set
            for name, value in options.items():
                self[name] = value

    def add(self, options):
        for key, value in options.items():
            self[key] = value

    def __setitem__(self, key, val):
        if key not in self.__allowed:
            raise InvalidOptionException(
                f'key: {key} not in allowed keys for RestrictedDict: {self.__allowed}'
            )
        dict.__setitem__(self, key, val)
