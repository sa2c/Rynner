# TODO behaviour should check that upload completed before end

# __init__(names, argument_mappings, defaults_arguments, default_formatter=format_and_append)
# context = self.behaviour.parse(options)
# isrunning = self.behaviour.run(self.connection, options)
# bool = self.behaviour.type(string)


class InvalidContextOption(Exception):
    pass


class Behaviour:
    def __init__(self, option_map, defaults):
        self.map = option_map

    # TODO why did I put connection here?
    def parse(self, connection, context):
        context = context.copy()

        options = []

        if 'script' in context.keys():
            script = context.pop('script')
        else:
            script = None

        curr_len = len(context.keys()) + 1

        while len(context.keys()) > 0:
            # if array length is unchanged, then an element has not been consumed
            # and an error should be thrown
            if curr_len == len(context.keys()):
                raise InvalidContextOption()
            curr_len = len(context.keys())
            for option in self.map:
                template = option[0]
                keys = option[1]

                # handle both single strings and tuples of strings
                # as tuples of strings
                if isinstance(keys, str):
                    keys = (keys, )

                # match if all keys in tuple are context keys
                if set(keys) <= set(context.keys()):
                    # format the template string using the list of keys (in order)
                    value_list = (context[key] for key in keys)
                    if callable(template):
                        # TODO - template can't currently decide that it will defer keys to a later function
                        # this could be useful, but could also be a source of errors if users forget to delete
                        # keys within the function
                        out = template(context, keys)
                    else:
                        out = template.format(*value_list)

                    # append formatted string to output
                    options.append(out)

                    # remove consumed keys from dict to avoid repetition
                    for key in keys:
                        del context[key]

                    break

        return {'options': options, 'script': script}

    def run(self, connection, context):
        pass
