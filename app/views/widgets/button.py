from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton
import PySide6.QtGui as QtGui

from sys import platform

class ButtonBox(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.__set_button_ui()

        # INFO: 判断当前的状态
        self.snip_res_flag = False
        self.img = None

    def __set_button_ui(self):
        # INFO: 截图按钮
        if platform == "darwin":
            self.snip_button = QPushButton('截图 [Shift+Option+S]')
            self.shortcut_snip = QtGui.QShortcut(QtGui.QKeySequence('Shift+Option+S'), self)
        else:
            self.snip_button = QPushButton('截图 [Shift+Alt+S]')
            self.shortcut_snip = QtGui.QShortcut(QtGui.QKeySequence('Shift+Alt+S'), self)
        # INFO: 识别按钮
        self.reco_button = QPushButton('OCR识别')
        self.reco_button.setEnabled(False)

        self.snip_button.setStyleSheet("""
            QPushButton {
                padding: 5px 10px;           /* 内边距 */
                min-width: 60px;             /* 最小宽度 */
            }
            QPushButton:hover {
                background-color: #f4645f;
                border:none;
            }
            QPushButton:pressed {
                background-color: #f4645f;   /* 按下时颜色 */
                padding-top: 9px;            /* 模拟下沉效果 */
                padding-bottom: 7px;
            }
        """)
        
        self.reco_button.setStyleSheet("""
            QPushButton {
                padding: 5px 10px;           /* 内边距 */
                min-width: 60px;             /* 最小宽度 */
            }
            QPushButton:hover {
                background-color: #f4645f;
                border:none;
            }
            QPushButton:pressed {
                background-color: #f4645f;   /* 按下时颜色 */
                padding-top: 9px;            /* 模拟下沉效果 */
                padding-bottom: 7px;
            }
        """)

        # INFO: 按钮的布局
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.snip_button)
        self.layout.addWidget(self.reco_button)