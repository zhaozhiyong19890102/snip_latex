from app.views.widgets.snip import SnipWidget
from app.controllers.snip_controller import SnipController
from app.controllers.button_controller import ButtonController
from app.controllers.menu_controller import MenuController
from app.controllers.tray_controller import TrayController

from PySide6.QtCore import Slot

class MainWindowController:
    def __init__(self, main_window_view):
        self.main_window_view = main_window_view
        self.snip_view = SnipWidget(main_window_view)
        self.button_view = self.main_window_view.button_box
        self.menu_view = self.main_window_view.menu_bar
        self.tray_view = self.main_window_view.tray
        # INFO: 按钮控制器
        self.button_controller = ButtonController(main_window_view, self.button_view, self)
        # INFO: 截图控制器
        self.snip_controller = SnipController(self.snip_view, main_window_view, self)
        # INFO: 菜单栏控制器
        self.menu_controller = MenuController(self.menu_view, main_window_view, self)
        # INFO: 托盘控制器
        self.tray_controller = TrayController(self.tray_view, main_window_view, self)
        # INFO: 设置状态位
        self.is_snipping = False

        self.main_window_view.latex_edit_box.latex_edit.textChanged.connect(self.__on_textbox_change)

    @Slot()
    def __on_textbox_change(self):
        text = self.main_window_view.latex_edit_box.latex_edit.toPlainText()
        self.button_controller.display_prediction(text)