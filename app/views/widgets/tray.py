from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PySide6.QtGui import QIcon, QAction

class Tray:
    def __init__(self, parent):
        self.parent = parent
        
        # INFO: 创建系统托盘图标
        self.tray_icon = QSystemTrayIcon(parent)
        self.tray_icon.setIcon(QIcon(':/icons/icon.svg'))
        self.tray_icon.setToolTip("SnipLatex")
        self.tray_icon.setVisible(False)  # 初始隐藏

        # INFO: 创建托盘菜单（右键菜单）
        self.__init_menu()

    def __init_menu(self):
        self.tray_menu = QMenu()
        # INFO: 菜单一
        self.restore_action = QAction("恢复窗口", self.parent)
        self.tray_menu.addAction(self.restore_action)
        # INFO: 菜单二
        self.quit_action = QAction("退出", self.parent)
        self.tray_menu.addAction(self.quit_action)

        self.tray_icon.setContextMenu(self.tray_menu)

        self.tray_menu.setStyleSheet(
            """
            QMenu::item:selected {background: #f4645f;}
            """)