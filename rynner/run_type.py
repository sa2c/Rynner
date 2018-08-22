from rynner.run import Run


class RunAction:
    def __init__(self, label, function):
        self.label = label
        self.function = function


class RunType:
    default_params = ["id"]

    def __init__(self, domain, name, interface, runner=None, params=None):
        self.name = name
        self.domain = domain
        self.interface = interface
        self.__actions = []
        self.runner = runner

        # set params to input, if specified otherwise set to default params
        if params is None:
            self.params = self.default_params
        else:
            self.params = params

    def create(self):
        # display configuration window
        accepted = self.interface.show()

        if accepted and len(self.interface.invalid()) == 0:
            data = self.interface.data()

            if self.runner is None:
                run = Run(**data)
            else:
                self.runner(data)

    def add_action(self, label, function):
        action = RunAction(label, function)
        self.__actions.append(action)
        return action

    def actions(self):
        return self.__actions
