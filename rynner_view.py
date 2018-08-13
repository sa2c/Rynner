import sys
from PySide2.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QApplication, QTextEdit, QVBoxLayout
from PySide2.QtCore import QSize


# an empty/blank QWidget wrapper?
class TextInput(QWidget):
    def __init__(self, key, label, parent=None, validation=None, default=None):
        super().__init__(parent)
        self.input = QTextEdit()
        self.validation = validation
        self.key = key
        self.default = default

        self.setLayout(QVBoxLayout())

        self.init()

    def value(self):
        return self.input.toPlainText()

    def valid(self):
        if self.validation is not None:
            return self.validation(self.value())
        else:
            return True

    def init(self):
        self.input.setText("tet")
        #self.addWidget(self.input)
        #self.label = QLabel("My Label")
        #self.addWidget(self.label)

    def addWidget(self, widget):
        self.layout().addWidget(widget)


#     def __init__(self,
#                  key,
#                  label,
#                  *args,
#                  parent=None,
#                  validation=None,
#                  **kwargs):

#         super().__init__(parent)
#         self.key = key
#         self.label = label
#         self.input = None

#     # This is called by the parent, if there is one, setting "parent"

#     def init(self, *args, **kwargs):
#         # override this function if necessary
#         # NEED TO ENSURE THIS IS OVERRIDEN...This creates examples
#         self.input = QTextEdit(self)
#         self.label = QLabel("My Label")
#         self.addWidget(self.label)
#         self.addWidget(self.input)

#     def valid(self):
#         ## stores and returns validation (so the QWidget does not need to)
#         if validation is not None:
#             return self.validation(self.value())

#     def value(self):
#         #if leaf
#         return self.input.value()

#         #if parent
#         return [child.value for child in self.children]

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
