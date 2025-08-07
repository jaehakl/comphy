import time, shutil, os, random, socket, subprocess, uuid
import numpy as np

from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

from functools import partial

from lib.state import *
from lib.task import Tasks, AbstractTask

from components.basic import TextComponent, LineEditComponent, ButtonComponent
from components.controls import SliderComponent
from components.mplchart import MplPlotComponent

class MainWindow(QMainWindow):
    def __init__(self):    
        super().__init__()

        #본 프로그램에서 Widget과 Component 들이 공유할 데이터 등록
        State().use("text",["3"])
        State().use("status",["Ready"])
        State().use("layers_t",[0, 100])
        State().use("layers_n",[1, 1.47])
        State().use("layers_k",[0, 0.001])
        State().use("spectrum",[[0,0,0],[1,1,1]])

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
        MplPlotComponent(id="spectrum", label="Spectrum", layout=mainLayout,
            model_id="spectrum")
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
        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignTop)
        self.render()

    def render(self):
        for i in range(self.layout().count()):
            self.layout().itemAt(i).widget().deleteLater()

        #Component 등록
        layers = State().get("layers_t")
        for i, layer in enumerate(layers):
            widget = QWidget()
            widget.setLayout(QHBoxLayout())
            self.layout().addWidget(widget)

            TextComponent(id="layer_label"+str(i), label="Layer "+str(i), layout=widget.layout(),
                model_id = "layers_t", model_index = i)
            SliderComponent(id="layer_t_"+str(i), label="T", layout=widget.layout(),
                scale = 5, min=0, max = 200,
                onChange = partial(self.editLayer, "t", i),
                model_id = "layers_t", model_index = i)
            LineEditComponent(id="layer_n_"+str(i), label="n", layout=widget.layout(),
                onChange = partial(self.editLayer, "n", i),
                model_id = "layers_n", model_index = i)
            LineEditComponent(id="layer_k_"+str(i), label="k", layout=widget.layout(),
                onChange = partial(self.editLayer, "k", i),
                model_id = "layers_k", model_index = i)
            ButtonComponent(id="insert_btn"+str(i), label="+", layout=widget.layout(),
                onClick = partial(self.addLayer, i))
            ButtonComponent(id="delete_btn"+str(i), label="-", layout=widget.layout(),
                onClick = partial(self.delLayer, i))
        ButtonComponent(id="submit", label="Calculate", layout=self.layout(),
            onClick = self.submit)

    def addLayer(self, i):
        State().insert("layers_t", 0, i+1)
        State().insert("layers_n", 1, i+1)
        State().insert("layers_k", 0, i+1)
        self.render()

    def delLayer(self, i):
        State().delete("layers_t", i)
        State().delete("layers_n", i)
        State().delete("layers_k", i)
        self.render()

    def editLayer(self, key, i, value):
        State().set("layers_"+key, float(value), i)
        self.submit()

    def submit(self):
        layers = []
        for i in range(len(State().get("layers_t"))):
            layers.append([
                State().get("layers_t")[i],
                State().get("layers_n")[i],
                State().get("layers_k")[i],
            ])
        Tasks().set("get_spectrum",
            GetSpectrum(layers),
            func_update=None,
            func_return=partial(State().set, "spectrum"))

class GetSpectrum(AbstractTask):
    def run(self):
        layers = self.args[0]    
        result = []
        self.update_value = None       
        for i in range(390, 831):
            fm = np.array([[1,0],[0,1]])
            if len(layers) >= 2:
                depth = 0                                
                for i_layer, layer in enumerate(layers):                    
                    if i_layer < len(layers)-1:
                        tm = self.get_transfer_matrix(layers[i_layer], layers[i_layer+1],i, depth)
                        fm = np.matmul(tm,fm)
                        depth += float(layers[i_layer+1][0])
                    elif i_layer == len(layers)-1:
                        tm = self.get_transfer_matrix(layers[i_layer], [0,1,0], i, depth)
                        fm = np.matmul(tm,fm)
                r = fm[1,0]/fm[1,1]
                t = fm[0,0]-fm[0,1]*r
                result.append([i, np.abs(r)**2, np.abs(t)**2])
            else:
                result.append([i, 0, 1])

        self.return_value = result
        return None

    def get_transfer_matrix(self, layer1, layer2, wavelength, depth):
        c1 = (float(layer1[1]) + 1j* float(layer1[2]))*2*np.pi/wavelength
        c2 = (float(layer2[1]) + 1j* float(layer2[2]))*2*np.pi/wavelength    

        q00 = (c2+c1)/(2*c2)*np.exp(1j*(c1-c2)*depth)
        q01 = (c2-c1)/(2*c2)*np.exp(1j*(-c2-c1)*depth)
        q10 = (c2-c1)/(2*c2)*np.exp(1j*(c2+c1)*depth)
        q11 = (c2+c1)/(2*c2)*np.exp(1j*(-c1+c2)*depth)

        return np.array([[q00,q01],[q10,q11]])

if __name__=="__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    app.setStyle('Fusion')
    app.exec()