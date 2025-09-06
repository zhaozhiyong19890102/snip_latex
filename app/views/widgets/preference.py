from PySide6.QtWidgets import QDialog, QPushButton, QSizePolicy, QGroupBox, QHBoxLayout, QRadioButton, QVBoxLayout, QWidget

from PySide6.QtGui import QIcon
from PySide6.QtCore import Slot

class ButtonBox(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

        self.button_group_box = QHBoxLayout(self)
        self.ok_button = QPushButton("确定")
        self.cancel_button = QPushButton("取消")
        self.button_group_box.addWidget(self.ok_button)
        self.button_group_box.addWidget(self.cancel_button)

        # 连接信号
        self.ok_button.clicked.connect(self.__config_fix)
        self.cancel_button.clicked.connect(parent.reject)

        self.ok_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.cancel_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.ok_button.setStyleSheet(
            """
            QPushButton {
                background-color: #C0C0C0;
                color: black;
                border: 1px solid #f4645f;
                padding: 5px 10px;           /* 内边距 */
                min-width: 60px;             /* 最小宽度 */
            }
            QPushButton:hover {
                background-color: #f4645f;
                border: none;
                color: white;
            }
            QPushButton:pressed {
                background-color: #f4645f;   /* 按下时颜色 */
                padding-top: 9px;            /* 模拟下沉效果 */
                padding-bottom: 7px;
            }
            """)
        
        self.cancel_button.setStyleSheet(
            """
            QPushButton {
                background-color: #C0C0C0;
                color: black;
                border: 1px solid #f4645f;
                padding: 5px 10px;           /* 内边距 */
                min-width: 60px;             /* 最小宽度 */
            }
            QPushButton:hover {
                background-color: #f4645f;
                border: none;
                color: white;
            }
            QPushButton:pressed {
                background-color: #f4645f;   /* 按下时颜色 */
                padding-top: 9px;            /* 模拟下沉效果 */
                padding-bottom: 7px;
            }
            """)
    
    @Slot()
    def __config_fix(self):
        close_flag = self.parent.config.config.get('UI', 'close_flag', fallback="close")
        actual_flag = "close"
        if not self.parent.button_close.isChecked():
            actual_flag = "tray"

        if close_flag != actual_flag:
            self.parent.config.save_info('UI', 'close_flag', actual_flag)
        self.parent.accept()  

class PreferenceDialog(QDialog):
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.setWindowTitle("设置")
        self.setWindowIcon(QIcon(":/icons/preference.svg"))
        self.setMinimumSize(200, 100)

        # INFO: 配置文件
        self.config = config

        self.group_box_close_flag = QGroupBox("设置关闭", self)
        layout_group_box = QHBoxLayout()
        self.button_close = QRadioButton("关闭")
        self.button_tray = QRadioButton("托盘")

        self.button_close.setStyleSheet(
            """
            QRadioButton::indicator {
                width: 10px;
                height: 10px;
                border-radius: 5px;  /* 圆角半径 = 10px（宽度/2） */
                border: 1px solid gray;
            }
            QRadioButton::indicator:hover {
                border: 1px solid #f4645f;  /* 悬停时边框变红 */
            }
            QRadioButton::indicator:checked {
                background-color: #f4645f;
                border: 1px solid #f4645f;
            }
            """
        )

        self.button_tray.setStyleSheet(
            """
            QRadioButton::indicator {
                width: 10px;
                height: 10px;
                border-radius: 5px;  /* 圆角半径 = 10px（宽度/2） */
                border: 1px solid gray;
            }
            QRadioButton::indicator:hover {
                border: 1px solid #f4645f;  /* 悬停时边框变红 */
            }
            QRadioButton::indicator:checked {
                background-color: #f4645f;
                border: 1px solid #f4645f;
            }
            """
        )

        layout_group_box.addWidget(self.button_close)
        layout_group_box.addWidget(self.button_tray)
        self.group_box_close_flag.setLayout(layout_group_box)

        self.button_group = ButtonBox(self)

        # 布局管理
        layout = QVBoxLayout()
        layout.addWidget(self.group_box_close_flag)
        layout.addWidget(self.button_group)
        self.setLayout(layout)

    def showEvent(self, event):
        super().showEvent(event)  # 调用父类方法确保正常显示
        close_flag = self.config.config.get('UI', 'close_flag', fallback="close")
        if close_flag == "close":
            self.button_close.setChecked(True)
        else:
            self.button_tray.setChecked(True)