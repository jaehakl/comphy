import time, shutil, os, random, socket, subprocess, uuid

from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

from functools import partial

from lib.state import *
from lib.task import Tasks, AbstractTask

from components.basic import TextComponent, ButtonComponent

class MainWindow(QMainWindow):
    def __init__(self):    
        super().__init__()

        #본 프로그램에서 Widget과 Component 들이 공유할 데이터 등록
        State().use("text",["3"])
        State().use("status",["Ready"])

        #Widget 등록        
        self.setMenuBar(MenuBar(self))
        self.addToolBar(ToolBar(self))
        self.setCentralWidget(CentralWidget())
        self.setSideWidget("Left",LeftWidget(), Qt.LeftDockWidgetArea)
        self.setSideWidget("Right",QWidget(), Qt.RightDockWidgetArea)
        self.setSideWidget("Bottom",QWidget(), Qt.BottomDockWidgetArea)
        self.setStatusBar(StatusBar(self))
        
        #메인 윈도우 환경 설정
        self.setWindowTitle("test")
        self.resize(500,500)
        self.setCorner(Qt.BottomLeftCorner, Qt.LeftDockWidgetArea)
        self.setCorner(Qt.BottomRightCorner, Qt.RightDockWidgetArea)

    def setSideWidget(self, title, widget, area):
        dockwidget = QDockWidget(title, self)
        dockwidget.setWidget(widget)
        self.addDockWidget(area, dockwidget)

class MenuBar(QMenuBar):
    def __init__(self, parent):
        super().__init__(parent)
        file_menu = QMenu("File", parent)
        file_menu.addAction("file_action_test")
        self.addMenu(file_menu)
        self.triggered.connect(lambda action: print(action.text()))

class ToolBar(QToolBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.addAction("action_test")
        self.addAction("action_test2")
        self.actionTriggered.connect(self.set_some_task)

    def set_some_task(self, action):
        if action.text() == "action_test":
            Tasks().set("update_text",UpdateText(1,2,3), 
                func_update=partial(setPartialState, "status", 0),
                func_return=partial(setPartialState, "status", 0))
        elif action.text() == "action_test2":
            Tasks().set("update_text2",UpdateText(1,2,3), 
                func_update=partial(setPartialState, "text", 0),
                func_return=partial(setPartialState, "text", 0))

class UpdateText(AbstractTask):
    def run(self):
        print(self.args)
        for i in range(1000):

            time.sleep(0.1)

            self.update_value = str(i)
        self.return_value = "finished"
        return None

class StatusBar(QStatusBar):
    def __init__(self, parent):
        super().__init__(parent)
        State().bind("status","statusbar_msg", self.showMessage, 0)

class CentralWidget(QWidget):
    def __init__(self):   
        super().__init__()

        #레이아웃 등록
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)

        #Component 등록
        TextComponent(id="text_test", label="Test Text", layout=mainLayout,
            model_id = "text", model_index = 0)
        ButtonComponent(id="btn_test", label="test1", layout=mainLayout,
            onClick = partial(self.update_text, "1"))
        ButtonComponent(id="btn_test2", label="test2", layout=mainLayout,
            onClick = lambda : State().set("text","2",0))
    
    #Method 정의
    def update_text(self, text):
        State().set("text",text,0)

class LeftWidget(QWidget):
    def __init__(self):   
        super().__init__()

        #레이아웃 등록
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)

        #Component 등록
        TextComponent(id="text_test", label="Test Text", layout=mainLayout,
            text = "left")

if __name__=="__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    app.setStyle('Fusion')
    app.exec()