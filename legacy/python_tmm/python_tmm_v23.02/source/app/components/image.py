from functools import partial

#Component 정의
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

from PIL.ImageQt import ImageQt
from PIL import Image
import io

from components.common_functions import bind_state

def ImageListComponent(id, layout, itemSelected=print, model=None):
    itemLayout = QVBoxLayout()
    layout.addLayout(itemLayout)

    def setImageList(imgDict):
        for i in range(itemLayout.count()):
            itemLayout.itemAt(i).widget().deleteLater()
        for key in imgDict.keys():
            img = imgDict[key]       

            imageItem = ImageLinkItem(key, img, 
                parent=layout.parentWidget())
            itemLayout.addWidget(imageItem)
            imageItem.linkActivated.connect(lambda id: itemSelected(id))

            img_label = QLabel(key,parent=layout.parentWidget())
            itemLayout.addWidget(img_label)

    if model is not None:
        bind_state(model, setImageList)

class ImageLinkItem(QLabel):
    def __init__(self, id, img, parent=None):
        super().__init__(id, parent)
        self.id = id
        qim = ImageQt(img)
        pix = QPixmap.fromImage(qim)
        self.setPixmap(QPixmap(pix))

    def mousePressEvent(self, e):
        if e.button()==Qt.LeftButton:
            self.linkActivated.emit(self.id)

def ImageComponent(id, label, layout, model=None, img=None):
    itemLayout = QHBoxLayout()
    layout.addLayout(itemLayout)

    imageItem = QLabel(label, layout.parentWidget())
    itemLayout.addWidget(imageItem)

    def setImage(img):
        if img != None:
            qim = ImageQt(img)
            pix = QPixmap.fromImage(qim)
            imageItem.setPixmap(QPixmap(pix))

    if model is not None:
        bind_state(model, setImage)
