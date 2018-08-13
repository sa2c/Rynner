class RynnerView:
    WidgetInstanceClass = ...
    widget_args = ...
    validation = ...

    def __init__(self, key, label, validation=..., instance_class=..., widget_args=..., **kwargs):
        self. ... = ...

    def build(self, gui-tk-symbol):
        '''build method'''
        # ...either returns itself it it's a leaf or recurses if it's branch
        # looks up the appropriate type to return based on gui-tk-symbol key
        map kwargs -> widget-args

        widget = self.WidgetInstanceClass(**widget_args, label=... validation=VALIDATION, mapping=MAPPING)

        return widget

class QRynnerWidget(QWidget):
    '''The thing which is constructed'''
    def __init__(type, validation, mapping):
        self... = ...

    def valid(self):
        pass

    def value(self):
        pass

    def draw(self): #? probably not....
        pass

    def value(self):
        return -> same structure as before, a list of (machine_key, value) pairs something else

class RynnerCommandLineWidget(QWidget):
    def __init__(type, validation, mapping):
        self... = ...

    def valid(self):
        pass

    def value(self):
        pass

    def run(self): #? probably yes in this case....
        pass

class QRynnerDialog(QWidget):
    def __init__(self, child):

    def value(self):
        flatten(child.value())
        # check for duplicate keys at output list construction

class RynnerCommandLineManager(QWidget):
    def __init__(self, child):

    def value(self):
        flatten(child.value())
        # check for duplicate keys at output list construction
