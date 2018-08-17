import sys
from PySide2.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QApplication, QLineEdit, QVBoxLayout, QDialog
from PySide2.QtCore import QSize, Signal

# an empty/blank QWidget wrapper?
# TODO : validation
# TODO : clis should do something sensible on exception (e.g. loop)
# TODO some reset method to reset the value to default (so it doesn't maintain previous value)


class Interface:
    def __init__(self, children):
        self.dialog = QDialog()
        self.children = children

        self.dialog.setLayout(QVBoxLayout())
        for child in self.children:
            self.dialog.layout().addWidget(child.widget())

    def show(self):
        self.dialog.show()

    def data(self):
        data = []
        for child in self.children:
            key = child.key()
            value = child.value()

            data[key] = value

        return data

    def valid(self):
        raise Exception("TESTING THIS")
        invalid_children = [
            child for child in self.children if not child.valid
        ]

        if len(invalid_children) == 0:
            return True
        else:
            return False, invalid_children


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

    # TODO : implement validation and test return result
    def valid(self):
        True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = TextInput('key', 'Test Input')
    widget.show()
    sys.exit(app.exec_())
