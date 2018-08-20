class InvalidContextOption(Exception):
    pass


class ScriptNotSpecifiedException(Exception):
    pass


class Behaviour:
    def __init__(self, option_map, defaults):
        self.map = option_map

    def parse(self, options):
        options = options.copy()

        # create a new context, this will later get passed to the run method
        context = []

        # script is handled differently, it lives in a seperate key
        if 'script' in options.keys():
            script = options.pop('script')
        else:
            raise ScriptNotSpecifiedException(
                "script key/argument is mandatory")

        curr_len = len(options.keys()) + 1

        # parse the options based on the option map, whilst there are still elements left
        while len(options.keys()) > 0:
            # array length unchanged implies elements which are not in the map
            if curr_len == len(options.keys()):
                invalid_keys = ', '.join(list(options.keys()))
                raise InvalidContextOption(
                    'invalid option(s): {}'.format(invalid_keys))
            curr_len = len(options.keys())

            for option in self.map:
                template = option[0]
                keys = option[1]

                # handle both single strings and tuples of strings
                # as tuples of strings
                if isinstance(keys, str):
                    keys = (keys, )

                # match if all keys in tuple are options keys
                if set(keys) <= set(options.keys()):
                    # format the template string using the list of keys (in order)
                    value_list = (options[key] for key in keys)
                    if callable(template):
                        out = template(options, keys)
                    else:
                        out = template.format(*value_list)

                    # append formatted string to output
                    context.append(out)

                    # remove consumed keys from dict to avoid repetition
                    for key in keys:
                        del options[key]

                    break

        return {'options': context, 'script': script}

    def run(self, connection, context):
        pass
