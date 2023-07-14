from functools import partial

#Component 정의
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from PIL.ImageQt import ImageQt
from PIL import Image
import io

from lib.state import State

def MplPlotComponent(id, label, layout, model_id=None, model_index=None):
    widget = FigureCanvasQTAgg(Figure())
    layout.addWidget(widget)
    plot = widget.figure.add_subplot()

    def setPlot(data_list):
        plot.clear()
        data_np = np.array(data_list).T

        for lindata in data_np[1:]:
            plot.plot(data_np[0], lindata)        
        widget.draw()
    
    if model_id is not None:
        State().bind(model_id, id, setPlot, model_index)