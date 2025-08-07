#Component 정의
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

from components.common_functions import bind_state

def TextComponent(id, label, layout, model_id=None, model=None, text=None):
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

    if model is not None:
        bind_state(model, setValue)


def LineEditComponent(id, label, layout, onChange=None, model = None, text=None):
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

    if model is not None:
        bind_state(model, setValue)

def ButtonComponent(id, label, layout, onClick=None):
    buttonItem = QPushButton(label)
    layout.addWidget(buttonItem)
    if onClick is not None:
        buttonItem.clicked.connect(onClick)