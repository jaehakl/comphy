#Component 정의
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

from lib.state import State

def TextComponent(id, label, layout, model_id=None, model_index=None, text=None):
    itemLayout = QHBoxLayout()
    widget = QWidget()
    widget.setLayout(itemLayout)
    layout.addWidget(widget)

    labelItem = QLabel(label)
    itemLayout.addWidget(labelItem)
    textItem = QLabel(text)
    itemLayout.addWidget(textItem)

    def setValue(value):
        textItem.setText(str(value))

    if model_id is not None:
        State().bind(model_id, id, setValue, model_index)


def LineEditComponent(id, label, layout, onChange=None, model_id=None, model_index=None, text=None):
    itemLayout = QHBoxLayout()
    widget = QWidget()
    widget.setLayout(itemLayout)
    layout.addWidget(widget)

    labelItem = QLabel(label)
    itemLayout.addWidget(labelItem)
    textItem = QLineEdit(text)
    itemLayout.addWidget(textItem)

    def setValue(value):
        textItem.setText(str(value))

    if onChange is not None:
        textItem.textChanged.connect(onChange)

    if model_id is not None:
        State().bind(model_id, id, setValue, model_index)


def ButtonComponent(id, label, layout, onClick=None):
    buttonItem = QPushButton(label)
    layout.addWidget(buttonItem)
    if onClick is not None:
        buttonItem.clicked.connect(onClick)