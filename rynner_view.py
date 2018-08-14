import sys
from PySide2.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QApplication, QLineEdit, QVBoxLayout
from PySide2.QtCore import QSize


# an empty/blank QWidget wrapper?
# TODO : validation
class TextInput(QWidget):
    def __init__(self, key, label, parent=None, default=None, reset=False):
        super().__init__(parent)
        self.input = QLineEdit(self)
        self.label = QLabel(label, self)
        self.key = key
        self.default_value = default

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.label)
        self.layout().addWidget(self.input)

        self.input.setText(self.default_value)

    def value(self):
        return self.input.text()

    def set_value(self, value):
        return self.input.setText(value)

    def reset(self):
        raise NotImplemented()
        if self.default_value is not None:
            self.input.setText(self.default_value)


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
