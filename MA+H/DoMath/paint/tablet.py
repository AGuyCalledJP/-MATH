import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class TabletSampleWindow(QWidget):
    def __init__(self, parent=None):
        super(TabletSampleWindow, self).__init__(parent)
        self.pen_is_down = False
        self.pen_x = 0
        self.pen_y = 0
        self.pen_pressure = 0
        self.text = ""
        self.drawing = False
        self.brushSize = 2
        self.brushColor = Qt.black
        self.lastPoint = QPoint()

        # Resizing the sample window to full desktop size:
        frame_rect = app.desktop().frameGeometry()
        width, height = frame_rect.width(), frame_rect.height()
        self.resize(600, 600)
        self.move(0, 0)
        self.setWindowTitle("MA+H")

    def tabletEvent(self, tabletEvent):
        self.pen_x = tabletEvent.globalX()
        self.pen_y = tabletEvent.globalY()
        self.pen_pressure = int(tabletEvent.pressure() * 100)
        if tabletEvent.type() == QTabletEvent.TabletPress:
            self.pen_is_down = True
            self.text = "TabletPress event"
        elif tabletEvent.type() == QTabletEvent.TabletMove:
            self.pen_is_down = True
            self.text = "TabletMove event"
        elif tabletEvent.type() == QTabletEvent.TabletRelease:
            self.pen_is_down = False
            self.text = "TabletRelease event"
        self.text += " at x={0}, y={1}, pressure={2}%,".format(self.pen_x, self.pen_y, self.pen_pressure)
        if self.pen_is_down:
            self.text += " Pen is down."
        else:
            self.text += " Pen is up."
        tabletEvent.accept()
        self.update()

    def mouseclickEvent(self, event): 
        if event.button() is Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

    def mousemoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self)
            painter.setPen(self.brushColor, self.brushSize, Qt.SolidLine)
            painter.drawLine(self.lastPoint,event.pos())
            self.lastPoint = event.pos()
            self.update()

    def mousereleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False


    def paintEvent(self, event):
        text = self.text
        i = text.find("\n\n")
        if i >= 0:
            text = text.left(i)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.TextAntialiasing)
        painter.drawText(self.rect(), Qt.AlignTop | Qt.AlignLeft , text)

app = QApplication(sys.argv)
mainform = TabletSampleWindow()
mainform.show()
app.exec_()