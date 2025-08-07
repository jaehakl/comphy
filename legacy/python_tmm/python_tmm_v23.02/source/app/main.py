import time, shutil, os, random, socket, subprocess, uuid
import numpy as np

from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

from functools import partial

from lib.state import AbstractState
from lib.task import Tasks, AbstractTask

from modules._main_state import MainState
import modules.transfer_matrix_method as tmm

from components.basic import TextComponent, LineEditComponent, ButtonComponent
from components.controls import SliderComponent
from components.mplchart import MplPlotComponent


class MenuBar(QMenuBar):
    def __init__(self, parent):
        super().__init__(parent)
        file_menu = QMenu("File", parent)
        file_menu.addAction("file_action_test")
        self.addMenu(file_menu)
        self.triggered.connect(lambda action: print(action.text()))


class MainWindow(QMainWindow):
    def __init__(self):    
        super().__init__()

        #Widget 등록        
        self.setMenuBar(MenuBar(self))

        #self.addToolBar(QToolBar(self))
        self.setCentralWidget(tmm.SpectrumViewWidget())
        self.setSideWidget("Layer Setting",tmm.LayerSetWidget(), Qt.RightDockWidgetArea)
        #self.setSideWidget("Right",QWidget(), Qt.RightDockWidgetArea)
        #self.setSideWidget("Bottom",QWidget(), Qt.BottomDockWidgetArea)

        self.setStatusBar(StatusBar(self))
        
        #메인 윈도우 환경 설정
        self.setWindowTitle("test")
        self.resize(1280,720)
        self.setCorner(Qt.BottomLeftCorner, Qt.LeftDockWidgetArea)
        self.setCorner(Qt.BottomRightCorner, Qt.RightDockWidgetArea)

    def setSideWidget(self, title, widget, area):
        dockwidget = QDockWidget(title, self)
        dockwidget.setWidget(widget)
        self.addDockWidget(area, dockwidget)


class StatusBar(QStatusBar):
    def __init__(self, parent):
        super().__init__(parent)
        MainState().bind("status","statusbar_msg", self.showMessage, 0)


if __name__=="__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    app.setStyle('Fusion')
    app.exec()