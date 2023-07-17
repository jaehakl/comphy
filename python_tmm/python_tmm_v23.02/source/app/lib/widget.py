from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

class AbstractWidget(QWidget):
    def __init__(self):   
        super().__init__()
        #레이아웃 등록
        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignTop)
        self.refresh()

    def refresh(self):
        for i in range(self.layout().count()):
            self.layout().itemAt(i).widget().deleteLater()
        widget = QWidget()
        widget.setLayout(QHBoxLayout())
        self.layout().addWidget(widget)

        self.render(widget)

    def render(self, widget):
        #TextComponent(id="text", label="Text", layout=widget.layout(),
        #        model=[State, "text", 0])
        pass

