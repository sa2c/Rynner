import sys
from abc import ABC, abstractmethod
from PySide2.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QFormLayout, QDialog, QDialogButtonBox, QGroupBox, QCheckBox
from PySide2.QtCore import QSize, Signal

# an empty/blank QWidget wrapper?
# TODO : validation
# TODO : clis should do something sensible on exception (e.g. loop)
# TODO some reset method to reset the value to default (so it doesn't maintain previous value)


class DuplicateKeyException(Exception):
    pass


class RunCreateView(QDialog):
    def __init__(self, fields, title="Set up run"):
        super().__init__(None)

        # store fields in instance
        self.fields = fields

        # check for duplicate keys
        seen = set()
        for field in fields:
            if field.key in seen:
                # raise an error if a duplicate key found
                raise DuplicateKeyException(
                    "duplicate entries for key '{}'".format(field.key))
            else:
                # collect seen keys, to check for duplicates
                seen.add(field.key)

        # layout fields
        container = QWidget()
        container.setLayout(QFormLayout())
        for field in self.fields:
            container.layout().addRow(field.label, field.widget)

        self.setWindowTitle(title)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(container)
        self._button_box = QDialogButtonBox(QDialogButtonBox.Ok
                                            | QDialogButtonBox.Cancel)
        self._button_box.accepted.connect(self.accept)
        self._button_box.rejected.connect(self.reject)
        self.layout().addWidget(self._button_box)

    def show(self):
        # reset field values
        [field.init() for field in self.fields]
        super().show()

    def data(self):
        return {field.key: field.value() for field in self.fields}

    def invalid(self):
        return [field for field in self.fields if not field.valid()]


class BaseField(ABC):
    '''
    A base class for input fields.

    Object of this class interface themself with Rynner through a key
    (or set of keys). The value(s) of the fields can be retrieved through the value()
    method.
    '''

    def __init__(self, key, label, default=None, remember=True):
        '''
        `key` : str
           The key in the corresponding dictionary 
           
        `widget` : QWidget
           The underlying Qt widget (which contains a layout and the set of checkboxes.)





        '''

        self.__default_value = default
        self.__remember = remember

        # public attributes
        self.key = key
        self.label = QLabel(label)
        self.widget = self._widget()

        # initialise with default value
        self.set_value(self.__default_value)

    @abstractmethod
    def _widget(self):
        pass

    @abstractmethod
    def value(self):
        pass

    @abstractmethod
    def set_value(self, value):
        pass

    def init(self):
        if not self.__remember:
            self.set_value(self.__default_value)

    def cli(self):
        return input(self.label.text())

    def valid(self):
        return True


class TextField(BaseField):
    def _widget(self):
        return QLineEdit()

    def value(self):
        return self.widget.text()

    def set_value(self, value):
        self.widget.setText(value)


class NumericField(TextField):
    def value(self):
        pass

    def set_value(self, value):
        pass


class CheckBoxesField(BaseField):
    ''' A set of checkboxes which can be interacted with separately.

    The dictionary of statuses (checked or not) can be retrieved with value().

    '''

    def __init__(
            self,
            keys,  # list N
            labels,  # list N
            title=None,
            defaults=None,  #list N
    ):
        '''
        `keys` : list of strings

        `labels` : list of strings
           Must have the same lenght as `keys`.

        `title` : str, optional
           The title of the widget, which contains all the checkboxes.

        `defaults` : List of bools, optional
           Default values. If provided, it must have the same length as `keys`.

        '''
        if defaults is None:
            defaults = [False for k in keys]

        if type(keys) != list:
            raise TypeError('"keys" is not a list.')
        if type(labels) != list:
            raise TypeError('"labels" is not a list.')
        if len(keys) != len(labels):
            raise ValueError(
                f'len(labels)[{len(labels)}] != len(keys)[{len(keys)}]')

        if len(defaults) != len(keys):
            raise ValueError(
                f'len(defaults)[{len(defaults)}] != len(keys)[{len(keys)}]')

        for key in keys:
            if type(key) is not str:
                raise TypeError('keys are not strings.')
        for label in labels:
            if type(label) is not str:
                raise TypeError('labels are not strings.')
        for default in defaults:
            if type(default) is not bool:
                raise TypeError('defaults are not booleans.')

        self.widget = self._widget(keys, labels, title, defaults)
        self.key = keys
        self.label = labels

    def _widget(self, keys, labels, title, defaults):
        w = QGroupBox(title)
        layout = QVBoxLayout()
        self._optionwidgets = {}
        self._layout = layout
        for key, label, default in zip(keys, labels, defaults):
            checkbox = QCheckBox(label)
            checkbox.setChecked(default)
            self._optionwidgets[key] = checkbox
            layout.addWidget(checkbox)
        w.setLayout(layout)
        return w

    def value(self):
        ''' Returns a dictionary containing the statuses for the checkboxes.'''
        values = {}
        for k in self.key:
            values[k] = self._optionwidgets[k].isChecked()

        return values

    def set_value(self, value_to_set):
        if type(value_to_set) is not dict:
            raise TypeError('Input is not a dictionary.')
        for v in value_to_set.values():
            if type(v) is not bool:
                raise TypeError('Input dict values are not booleans.')

        for k, v in value_to_set.items():
            self._optionwidgets[k].setChecked(v)
