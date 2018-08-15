import sys
from PySide2.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QApplication, QLineEdit, QVBoxLayout
from PySide2.QtCore import QSize, Signal


# an empty/blank QWidget wrapper?
# TODO : validation
class TextInput:
    def __init__(self, key, label, default=None, remember=True):

        self.widget = QWidget()

        self.__key = key
        self.default_value = default
        self.widget.setLayout(QVBoxLayout())
        self.remember = remember
        self.label = label

        for widget in self.widgets():
            self.widget.layout().addWidget(widget)

        self.set_value(self.default_value)

    def widgets(self):
        self.input = QLineEdit(self.widget)
        return [QLabel(self.label, self.widget), self.input]

    def value(self):
        return self.input.text()

    def set_value(self, value):
        return self.input.setText(value)

    def key(self):
        return self.__key

    def init(self):
        if not self.remember:
            self.set_value(self.default_value)

    # TODO some reset method to reset the value to default (so it doesn't maintain previous value)


#     def cli(self):
#         valid = False
#         while not valid:
#             print("Label: {}".format(self.label))
#             # read from command line

#         return value

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = TextInput('key', 'Test Input')
    widget.show()
    sys.exit(app.exec_())
