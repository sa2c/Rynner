import sys
from PySide2.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QFormLayout, QDialog, QDialogButtonBox
from PySide2.QtCore import QSize, Signal

# an empty/blank QWidget wrapper?
# TODO : validation
# TODO : clis should do something sensible on exception (e.g. loop)
# TODO some reset method to reset the value to default (so it doesn't maintain previous value)


class DuplicateKeyException(Exception):
    pass


class RunnerConfigDialog(QDialog):
    def __init__(self, dialog_title, widget):
        super().__init__(None)
        self.setWindowTitle(dialog_title)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(widget)
        self._button_box = QDialogButtonBox(QDialogButtonBox.Ok
                                            | QDialogButtonBox.Cancel)
        self._button_box.accepted.connect(self.accept)
        self._button_box.rejected.connect(self.reject)
        self.layout().addWidget(self._button_box)


class Interface:
    def __init__(self, children):
        # store children in instance
        self.children = children

        # check for duplicate keys
        seen = set()
        for child in children:
            if child.key in seen:
                # raise an error if a duplicate key found
                raise DuplicateKeyException(
                    "duplicate entries for key '{}'".format(child.key))
            else:
                # collect seen keys, to check for duplicates
                seen.add(child.key)

        # layout children
        container = self.container()

        # intialise dialog with container
        self.dialog = RunnerConfigDialog("Configure Run", container)

    def container(self):
        widget = QWidget()
        widget.setLayout(QFormLayout())
        for child in self.children:
            widget.layout().addRow(child.label, child.widget)
        return widget

    def show(self):
        # reset values
        [child.init() for child in self.children]

        accepted = self.dialog.exec_()

        return accepted

    def data(self):
        return {child.key: child.value() for child in self.children}

    def invalid(self):
        return [child for child in self.children if not child.valid()]


class TextInput:
    def __init__(self, key, label, default=None, remember=True):

        self.__default_value = default
        self.__remember = remember

        # public attributes
        self.key = key
        self.label = QLabel(label)
        self.widget = QLineEdit()

        # initialise with default value
        self.set_value(self.__default_value)

    def value(self):
        return self.widget.text()

    def set_value(self, value):
        return self.widget.setText(value)

    def init(self):
        if not self.__remember:
            self.set_value(self.__default_value)

    def cli(self):
        return input(self.label.text())

    def valid(self):
        return True
