import sys
from PySide2.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QApplication, QLineEdit, QVBoxLayout, QDialog, QDialogButtonBox
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

    #MockConfigDialog().

    #dialog_exec_return = MockConfigDialog().exec()
    #self.assertEqual(accepted, dialog_exec_return)

    # dialog = QDialog()
    # dialog.setWindowTitle("Title")
    # dialog.setLayout(QVBoxLayout())
    # dialog.layout().addWidget(self.widget)
    # buttons = QDialogButtonBox(QDialogButtonBox.Ok
    #                            | QDialogButtonBox.Cancel)
    # dialog.layout().addWidget(buttons)

    # accepted = dialog.exec()
    # return accepted


class Interface:
    def __init__(self, children):
        self.widget = QWidget()

        # check for duplicate keys

        # store children as a dictionary
        self.children = {}

        self.widget.setLayout(QVBoxLayout())

        for child in children:
            key = child.key()
            value = child

            if key in self.children:
                raise DuplicateKeyException(
                    "duplicate entries for key '{}'".format(key))
            else:
                self.children[key] = value
                child.widget().setParent(self.widget)
                self.widget.layout().addWidget(child.widget())

    def show(self):
        # reset values
        [child.init() for child in self.children.values()]

        # show dialog
        config_dialog = RunnerConfigDialog("Configure Run", self.widget)

        accepted = config_dialog.exec()

        return accepted

    def data(self):
        data = {}
        for key, child in self.children.items():

            value = child.value()

            data[key] = value

        return data

    def invalid(self):
        return [child for child in self.children.values() if not child.valid()]


class TextInput:
    def __init__(self, key, label, default=None, remember=True):

        self.__widget = QWidget()

        self.__key = key
        self.default_value = default
        self.__widget.setLayout(QVBoxLayout())
        self.remember = remember
        self.label = label

        for widget in self.widgets():
            self.__widget.layout().addWidget(widget)

        self.set_value(self.default_value)

    def widgets(self):
        self.input = QLineEdit(self.__widget)
        return [QLabel(self.label, self.__widget), self.input]

    def value(self):
        return self.input.text()

    def set_value(self, value):
        return self.input.setText(value)

    def widget(self):
        return self.__widget

    def key(self):
        return self.__key

    def init(self):
        if not self.remember:
            self.set_value(self.default_value)

    def cli(self):
        return input(self.label)

    def valid(self):
        return True
