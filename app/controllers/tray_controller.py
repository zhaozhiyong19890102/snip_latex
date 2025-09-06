from PySide6.QtCore import Slot
from PySide6.QtWidgets import QApplication, QSystemTrayIcon

class TrayController:
    def __init__(self, tray_view, main_window_view, main_controller):
        self.tray_view = tray_view
        self.main_window_view = main_window_view
        self.main_controller = main_controller

        # INFO: 重建菜单
        self.tray_view.restore_action.triggered.connect(self.__restore_from_tray)
        # INFO: 退出程序
        self.tray_view.quit_action.triggered.connect(self.__true_quit)
        # INFO: 双击托盘图标恢复窗口
        self.tray_view.tray_icon.activated.connect(self.__on_tray_activated)

    @Slot()
    def __restore_from_tray(self):
        # INFO: 显示主窗口
        self.main_window_view.show()
        # INFO: 隐藏托盘图标
        self.tray_view.tray_icon.setVisible(False)
    
    @Slot()
    def __true_quit(self):
        # INFO: 真实退出程序（通过托盘菜单）
        self.tray_view.tray_icon.hide()
        QApplication.quit()

    @Slot()
    def __on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.__restore_from_tray()