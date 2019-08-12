from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from MainWindow import Ui_MainWindow
# from TheBrain import PinkyAnd
from DarkBrain import Run as R
from Expression import *

import os
import random
import types


BRUSH_MULT = 3
SPRAY_PAINT_MULT = 5
SPRAY_PAINT_N = 100

COLORS = [
    '#000000', '#82817f', '#820300', '#868417', '#007e03', '#037e7b', '#040079',
    '#81067a', '#7f7e45', '#05403c', '#0a7cf6', '#093c7e', '#7e07f9', '#7c4002',

    '#ffffff', '#c1c1c1', '#f70406', '#fffd00', '#08fb01', '#0bf8ee', '#0000fa',
    '#b92fc2', '#fffc91', '#00fd83', '#87f9f9', '#8481c4', '#dc137d', '#fb803c',
]

FONT_SIZES = [7, 8, 9, 10, 11, 12, 13, 14, 18, 24, 36, 48, 64, 72, 96, 144, 288]

# MODES = [
#     'selectpoly', 'selectrect',
#     'eraser', 'fill',
#     'dropper', 'stamp',
#     'pen', 'brush',
#     'spray', 'text',
#     'line', 'polyline',
#     'rect', 'polygon',
#     'ellipse', 'roundrect'
# ]

MODES = [
    'eraser', 'pen'
]

FUNCTIONS = [
     'run'
]

CANVAS_DIMENSIONS = 832,832

STAMP_DIR = './stamps'
STAMPS = [os.path.join(STAMP_DIR, f) for f in os.listdir(STAMP_DIR)]

SELECTION_PEN = QPen(QColor(0xff, 0xff, 0xff), 1, Qt.DashLine)
PREVIEW_PEN = QPen(QColor(0xff, 0xff, 0xff), 1, Qt.SolidLine)


def build_font(config):
    """
    Construct a complete font from the configuration options
    :param self:
    :param config:
    :return: QFont
    """
    font = config['font']
    font.setPointSize(config['fontsize'])
    font.setBold(config['bold'])
    font.setItalic(config['italic'])
    font.setUnderline(config['underline'])
    return font


class Canvas(QLabel):

    mode = 'rectangle'

    primary_color = QColor(Qt.black)
    secondary_color = None

    primary_color_updated = pyqtSignal(str)
    secondary_color_updated = pyqtSignal(str)

    # Store configuration settings, including pen width, fonts etc.
    config = {
        # Drawing options.
        'size': 6,
        'fill': True,
        # Font options.
        'font': QFont('Times'),
        'fontsize': 12,
        'bold': False,
        'italic': False,
        'underline': False,
    }

    active_color = None
    preview_pen = None

    timer_event = None

    current_stamp = None

    def initialize(self):
        self.background_color = QColor(self.secondary_color) if self.secondary_color else QColor(Qt.white)
        self.eraser_color = QColor(self.secondary_color) if self.secondary_color else QColor(Qt.white)
        self.eraser_color.setAlpha(100)
        self.reset()

    def reset(self):
        # Create the pixmap for display.
        self.setPixmap(QPixmap(*CANVAS_DIMENSIONS))

        # Clear the canvas.
        self.pixmap().fill(self.background_color)

    def set_primary_color(self, hex):
        self.primary_color = QColor(hex)

    def set_secondary_color(self, hex):
        self.secondary_color = QColor(hex)

    def set_config(self, key, value):
        self.config[key] = value

    def set_mode(self, mode):
        # Clean up active timer animations.
        self.timer_cleanup()
        # Reset mode-specific vars (all)
        self.active_shape_fn = None
        self.active_shape_args = ()

        self.origin_pos = None

        self.current_pos = None
        self.last_pos = None

        self.history_pos = None
        self.last_history = []

        self.current_text = ""
        self.last_text = ""

        self.last_config = {}

        self.dash_offset = 0
        self.locked = False
        # Apply the mode
        self.mode = mode

    def reset_mode(self):
        self.set_mode(self.mode)

    def on_timer(self):
        if self.timer_event:
            self.timer_event()

    def timer_cleanup(self):
        if self.timer_event:
            # Stop the timer, then trigger cleanup.
            timer_event = self.timer_event
            self.timer_event = None
            timer_event(final=True)

    # Mouse events.

    def mousePressEvent(self, e):
        fn = getattr(self, "%s_mousePressEvent" % self.mode, None)
        if fn:
            return fn(e)

    def mouseMoveEvent(self, e):
        fn = getattr(self, "%s_mouseMoveEvent" % self.mode, None)
        if fn:
            return fn(e)

    def mouseReleaseEvent(self, e):
        fn = getattr(self, "%s_mouseReleaseEvent" % self.mode, None)
        if fn:
            return fn(e)

    def mouseDoubleClickEvent(self, e):
        fn = getattr(self, "%s_mouseDoubleClickEvent" % self.mode, None)
        if fn:
            return fn(e)

    # Generic events (shared by brush-like tools)

    def generic_mousePressEvent(self, e):
        self.last_pos = e.pos()

        if e.button() == Qt.LeftButton:
            self.active_color = self.primary_color
        else:
            self.active_color = self.secondary_color

    def generic_mouseReleaseEvent(self, e):
        self.last_pos = None

    # Mode-specific events.

    # Eraser events

    def eraser_mousePressEvent(self, e):
        self.generic_mousePressEvent(e)

    def eraser_mouseMoveEvent(self, e):
        if self.last_pos:
            p = QPainter(self.pixmap())
            p.setPen(QPen(self.eraser_color, 30, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            p.drawLine(self.last_pos, e.pos())

            self.last_pos = e.pos()
            self.update()

    def eraser_mouseReleaseEvent(self, e):
        self.generic_mouseReleaseEvent(e)

    # Pen events

    def pen_mousePressEvent(self, e):
        self.generic_mousePressEvent(e)

    def pen_mouseMoveEvent(self, e):
        if self.last_pos:
            p = QPainter(self.pixmap())
            p.setPen(QPen(self.active_color, self.config['size'], Qt.SolidLine, Qt.SquareCap, Qt.RoundJoin))
            p.drawLine(self.last_pos, e.pos())

            self.last_pos = e.pos()
            self.update()

    def pen_mouseReleaseEvent(self, e):
        self.generic_mouseReleaseEvent(e)

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Replace canvas placeholder from QtDesigner.
        self.horizontalLayout.removeWidget(self.canvas)
        self.canvas = Canvas()
        self.canvas.initialize()

        # We need to enable mouse tracking to follow the mouse without the button pressed.
        self.canvas.setMouseTracking(True)

        # Enable focus to capture key inputs.
        self.canvas.setFocusPolicy(Qt.StrongFocus)
        self.horizontalLayout.addWidget(self.canvas)

        # Setup the mode buttons
        mode_group = QButtonGroup(self)
        mode_group.setExclusive(True)

        for mode in MODES:
            btn = getattr(self, '%sButton' % mode)
            btn.pressed.connect(lambda mode=mode: self.canvas.set_mode(mode))
            mode_group.addButton(btn)

        # Setup the mode buttons
        function_groups = QButtonGroup(self)
        function_groups.setExclusive(True)

        for func in FUNCTIONS:
            btn = getattr(self, '%sButton' % func)
            btn.pressed.connect(lambda func=func: self.run())
            function_groups.addButton(btn)

        # Setup up action signals
        self.actionCopy.triggered.connect(self.copy_to_clipboard)

        # Initialize animation timer.
        self.timer = QTimer()
        self.timer.timeout.connect(self.canvas.on_timer)
        self.timer.setInterval(100)
        self.timer.start()

        # Setup to agree with Canvas.
        self.set_primary_color('#000000')
        self.set_secondary_color('#ffffff')

        # Signals for canvas-initiated color changes (dropper).
        self.canvas.primary_color_updated.connect(self.set_primary_color)
        self.canvas.secondary_color_updated.connect(self.set_secondary_color)

        # Menu options
        self.actionNewImage.triggered.connect(self.canvas.initialize)
        self.actionOpenImage.triggered.connect(self.open_file)
        self.actionSaveImage.triggered.connect(self.save_file)
        self.actionClearImage.triggered.connect(self.canvas.reset)
        self.actionInvertColors.triggered.connect(self.invert)
        self.actionFlipHorizontal.triggered.connect(self.flip_horizontal)
        self.actionFlipVertical.triggered.connect(self.flip_vertical)

        sizeicon = QLabel()
        sizeicon.setPixmap(QPixmap(os.path.join('images', 'border-weight.png')))
        self.drawingToolbar.addWidget(sizeicon)
        self.sizeselect = QSlider()
        self.sizeselect.setRange(1,20)
        self.sizeselect.setOrientation(Qt.Horizontal)
        self.sizeselect.valueChanged.connect(lambda s: self.canvas.set_config('size', s))
        self.drawingToolbar.addWidget(self.sizeselect)

        self.show()

    def run(self):
        self.snapshot()
        R()
        # self.kowalskianalysis(res)

    def kowalskianalysis(self, res):
        res = res[0]
        e = Expression()
        a = Constant(res)
        e.addSubExpr(a)
        print(e)
        self.outputWindow.setText(str(e))
        self.outputWindow.update()

    def set_primary_color(self, hex):
        self.canvas.set_primary_color(hex)

    def set_secondary_color(self, hex):
        self.canvas.set_secondary_color(hex)

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()

        if self.canvas.mode == 'selectrect' and self.canvas.locked:
            clipboard.setPixmap(self.canvas.selectrect_copy())

        elif self.canvas.mode == 'selectpoly' and self.canvas.locked:
            clipboard.setPixmap(self.canvas.selectpoly_copy())

        else:
            clipboard.setPixmap(self.canvas.pixmap())

    def open_file(self):
        """
        Open image file for editing, scaling the smaller dimension and cropping the remainder.
        :return:
        """
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "PNG image files (*.png); JPEG image files (*jpg); All files (*.*)")

        if path:
            pixmap = QPixmap()
            pixmap.load(path)

            # We need to crop down to the size of our canvas. Get the size of the loaded image.
            iw = pixmap.width()
            ih = pixmap.height()

            # Get the size of the space we're filling.
            cw, ch = CANVAS_DIMENSIONS

            if iw/cw < ih/ch:  # The height is relatively bigger than the width.
                pixmap = pixmap.scaledToWidth(cw)
                hoff = (pixmap.height() - ch) // 2
                pixmap = pixmap.copy(
                    QRect(QPoint(0, hoff), QPoint(cw, pixmap.height()-hoff))
                )

            elif iw/cw > ih/ch:  # The height is relatively bigger than the width.
                pixmap = pixmap.scaledToHeight(ch)
                woff = (pixmap.width() - cw) // 2
                pixmap = pixmap.copy(
                    QRect(QPoint(woff, 0), QPoint(pixmap.width()-woff, ch))
                )

            self.canvas.setPixmap(pixmap)
    
    def save_file(self):
        """
        Save active canvas to image file.
        :return:
        """
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "PNG Image file (*.png)")

        if path:
            pixmap = self.canvas.pixmap()
            pixmap.save(path, "PNG" )

    def snapshot(self):
        """
        Save active canvas to image file.
        :return:
        """
        if os.path.isfile("run.jpg"):
            pwd = os.getcwd()
            end = os.listdir(pwd + "/runoff/")
            os.rename(pwd + "/run.jpg",(pwd + "/runoff/run" + str(len(end)) + ".jpg"))
        pixmap = self.canvas.pixmap()
        pixmap.save('run.jpg', "JPG" )

    def invert(self):
        img = QImage(self.canvas.pixmap())
        img.invertPixels()
        pixmap = QPixmap()
        pixmap.convertFromImage(img)
        self.canvas.setPixmap(pixmap)

    def flip_horizontal(self):
        pixmap = self.canvas.pixmap()
        self.canvas.setPixmap(pixmap.transformed(QTransform().scale(-1, 1)))

    def flip_vertical(self):
        pixmap = self.canvas.pixmap()
        self.canvas.setPixmap(pixmap.transformed(QTransform().scale(1, -1)))



if __name__ == '__main__':

    app = QApplication([])
    window = MainWindow()
    app.exec_()