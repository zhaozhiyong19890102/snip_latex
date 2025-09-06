from PySide6.QtWidgets import QMainWindow
from screeninfo import get_monitors
from numpy import array
from PySide6.QtCore import QPoint, QTimer
from pynput.mouse import Controller
import PySide6.QtGui as QtGui

class SnipWidget(QMainWindow):
    is_snipping = False

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        # INFO: 获取所有显示器的支持
        monitos = get_monitors()
        bboxes = array([[m.x, m.y, m.width, m.height] for m in monitos])
        x, y, _, _ = bboxes.min(0)
        w, h = bboxes[:, [0, 2]].sum(1).max(), bboxes[:, [1, 3]].sum(1).max()
        self.setGeometry(x, y, w-x, h-y)

        self.begin = QPoint()
        self.end = QPoint()

        self.mouse = Controller()

        # Create and start the timer
        self.factor = QtGui.QGuiApplication.primaryScreen().devicePixelRatio()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_geometry_based_on_cursor_position)
        self.timer.start(500)

    def update_geometry_based_on_cursor_position(self):
        if not self.is_snipping:
            return

        # Update the geometry of the SnipWidget based on the current screen
        mouse_pos = QtGui.QCursor.pos()
        screen = QtGui.QGuiApplication.screenAt(mouse_pos)
        if screen:
            self.factor = screen.devicePixelRatio()
            screen_geometry = screen.geometry()
            self.setGeometry(screen_geometry)