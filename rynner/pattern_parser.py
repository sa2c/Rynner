import re


class InvalidContextOption(Exception):
    pass


class ScriptNotSpecifiedException(Exception):
    pass


class PatternParser:
    '''This models a scheduler (slurm, pbs, lsf,...)

    The information about how the scheduler works is stored in a 'host_pattern'
    object. See the module :mod:`host_patterns<rynner.host_patterns>`, and the
    :data:`host_pattern dictionary<rynner.host_patterns.host_patterns>`.

    '''

    def __init__(self, parameter_map, submit_cmd, defaults):
        '''
        Parameters
        ----------
        `parameter_map` : TODO docs
            TODO docs
        `submit_cmd` : TODO docs
            TODO docs
        `defaults` : TODO docs
           TODO docs

        '''
        self._map = parameter_map
        self._submit_cmd = submit_cmd

    def parse(self, options):
        '''Parses given options

        Parameters
        ----------
        `options` : dict
           TODO docs



        Returns
        -------
        `context` : dict
           A dictionary with following keys:
           `options` : list of strings
               A list of strings representing the scheduler options
               (e.g. the #SBACH or #PBS directives).
           `script` : string
               The body of the script of the jobcard.

        '''
        options = options.copy()

        # create a new context_options, this will later get passed to the run method
        context_options = []

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

            for option in self._map:
                template = option[0]
                keys = option[1]

                # handle both single strings and tuples of strings
                # as tuples of strings
                if isinstance(keys, str):
                    keys = (keys, )

                # match if all keys in tuple are options keys
                if set(keys) <= set(options.keys()):
                    # format the template string using the list of keys (in order)
                    value_list = [options[key] for key in keys]
                    if value_list != [False]:
                        if callable(template):
                            out = template(options, keys)
                        else:
                            out = template.format(*value_list)
                        # append formatted string to output
                        context_options.append(out)

                    # remove consumed keys from dict to avoid repetition
                    for key in keys:
                        del options[key]

                    break

        context = {'options': context_options, 'script': script}

        return context

    def run(self, connection, context, remote_path):
        # collect a list of all the lines in the resultant jobcard
        lines = ['#!/bin/sh'] + context['options'] + [context['script']]

        # build the jobcard as a string
        jobcard = '\n'.join(lines) + '\n'

        # upload the jobcard to the cluster
        remote_jobcard = '/'.join([remote_path, 'jobcard'])
        connection.put_file_content(jobcard, remote_jobcard)

        # run using the submit command provided
        exitstatus, stdout, stderr = connection.run_command(
            self._submit_cmd, pwd=remote_path)

        return exitstatus, stdout, stderr
