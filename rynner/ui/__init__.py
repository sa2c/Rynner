import sys, os
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile

loader = QUiLoader()


def load_ui(filename):
    filepath = os.path.join(os.path.dirname(__file__), filename)

    file = QFile(filepath)
    file.open(QFile.ReadOnly)

    window = loader.load(file)
    return window
