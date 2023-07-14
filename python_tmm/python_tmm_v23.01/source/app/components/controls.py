#Component 정의
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

from lib.state import State

def SliderComponent(id, label, layout, scale=1, min=0, max=100,
        onChange=None, model_id=None, model_index=None, value=None):
    itemLayout = QHBoxLayout()
    widget = QWidget()
    widget.setLayout(itemLayout)
    layout.addWidget(widget)

    labelItem = QLabel(label)
    itemLayout.addWidget(labelItem)
    sliderItem = QSlider(Qt.Horizontal)
    itemLayout.addWidget(sliderItem)
    
    def setValue(v):
        if v != None:
            sliderItem.setValue(int(v/scale))

    setValue(value)

    if onChange is not None:
        sliderItem.valueChanged.connect(lambda v: onChange(v*scale))

    if model_id is not None:
        State().bind(model_id, id, setValue, model_index)

