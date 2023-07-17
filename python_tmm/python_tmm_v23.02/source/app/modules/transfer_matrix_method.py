import time, shutil, os, random, socket, subprocess, uuid
import numpy as np

from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

from functools import partial

from lib.state import AbstractState
from lib.task import Tasks, AbstractTask

from components.basic import TextComponent, LineEditComponent, ButtonComponent
from components.controls import SliderComponent
from components.mplchart import MplPlotComponent


class State(AbstractState):
    def __init__(self):
        super().__init__()
        self.use("layers_t",[0, 100])
        self.use("layers_n",[1, 1.47])
        self.use("layers_k",[0, 0.001])
        self.use("spectrum",[[0,0,0],[1,1,1]])


class SpectrumViewWidget(QWidget):
    def __init__(self):   
        super().__init__()

        #레이아웃 등록
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)

        #Component 등록
        MplPlotComponent(id="spectrum", label="Spectrum", layout=mainLayout,
            model=[State, "spectrum"])


class LayerSetWidget(QWidget):
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
                 model=[State, "layers_t", i])
            SliderComponent(id="layer_t_"+str(i), label="T", layout=widget.layout(),
                scale = 5, min=0, max = 200,
                onChange = partial(self.editLayer, "t", i),
                model=[State, "layers_t", i])
            LineEditComponent(id="layer_n_"+str(i), label="n", layout=widget.layout(),
                onChange = partial(self.editLayer, "n", i),
                model=[State, "layers_n", i])
            LineEditComponent(id="layer_k_"+str(i), label="k", layout=widget.layout(),
                onChange = partial(self.editLayer, "k", i),
                model=[State, "layers_k", i])
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