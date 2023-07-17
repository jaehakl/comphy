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

from components.common_functions import bind_state

def MplPlotComponent(id, label, layout, model=None):
    widget = FigureCanvasQTAgg(Figure())
    layout.addWidget(widget)
    plot = widget.figure.add_subplot()

    def setPlot(data_list):
        plot.clear()
        data_np = np.array(data_list).T

        for lindata in data_np[1:]:
            plot.plot(data_np[0], lindata)        
        widget.draw()
    
    if model is not None:
        bind_state(model, setPlot)
