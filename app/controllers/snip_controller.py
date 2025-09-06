from PySide6.QtCore import Qt, QRect, QPoint
import PySide6.QtGui as QtGui
from PySide6.QtWidgets import QApplication
from PIL import ImageGrab
from sys import platform

class SnipController:
    def __init__(self, snip_view, main_window_view, main_controller):
        self.snip_view = snip_view
        self.main_window_view = main_window_view

        self.main_controller = main_controller

        self.snip_view.paintEvent = self.paintEvent
        self.snip_view.keyPressEvent = self.keyPressEvent
        self.snip_view.mousePressEvent = self.mousePressEvent
        self.snip_view.mouseMoveEvent = self.mouseMoveEvent
        self.snip_view.mouseReleaseEvent = self.mouseReleaseEvent

    def snip(self):
        self.snip_view.is_snipping = True
        # INFO: 窗口置顶
        self.snip_view.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        # INFO: 设置十字光标
        QApplication.setOverrideCursor(QtGui.QCursor(Qt.CursorShape.CrossCursor))
        self.snip_view.show()

    def paintEvent(self, event):
        if self.snip_view.is_snipping:
            brushColor = (255, 255, 255, 0)
            opacity = 0.3
        else:
            brushColor = (255, 255, 255, 0)
            opacity = 0

        self.snip_view.setWindowOpacity(opacity) # 截图时的透明度
        qp = QtGui.QPainter(self.snip_view)
        if not qp.isActive():
            return
        try:
            qp.setPen(QtGui.QPen(QtGui.QColor('red'), 1)) # 边框
            qp.setBrush(QtGui.QColor(*brushColor))
            qp.drawRect(QRect(self.snip_view.begin, self.snip_view.end))
        finally:
            qp.end()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape.value:
            QApplication.restoreOverrideCursor()
            self.snip_view.close()
            self.main_window_view.show()
        event.accept()

    def mousePressEvent(self, event):
        self.snip_view.start_pos = self.snip_view.mouse.position

        self.snip_view.begin = event.pos()
        self.snip_view.end = self.snip_view.begin
        self.snip_view.update()

    def mouseMoveEvent(self, event):
        self.snip_view.end = event.pos()
        self.snip_view.update()

    def mouseReleaseEvent(self, event):
        self.snip_view.is_snipping = False
        QApplication.restoreOverrideCursor()

        start_pos = self.snip_view.start_pos
        end_pos = self.snip_view.mouse.position

        x1 = int(min(start_pos[0], end_pos[0]))
        y1 = int(min(start_pos[1], end_pos[1]))
        x2 = int(max(start_pos[0], end_pos[0]))
        y2 = int(max(start_pos[1], end_pos[1]))

        self.snip_view.repaint()
        QApplication.processEvents()
        try:
            img = ImageGrab.grab(bbox=(x1, y1, x2, y2), all_screens=True)
        except Exception as e:
            if platform == "darwin":
                img = ImageGrab.grab(bbox=(x1//self.factor, y1//self.factor,
                                           x2//self.factor, y2//self.factor), all_screens=True)
            else:
                raise e
        QApplication.processEvents()

        self.snip_view.close()
        self.snip_view.begin = QPoint()
        self.snip_view.end = QPoint()
        # INFO: 将结果送回到“裁剪”按钮
        self.main_controller.button_controller.ret_snip(img)