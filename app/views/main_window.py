from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QApplication
from PySide6.QtGui import QIcon

from app.views.widgets.menu import MenuBar
from app.views.widgets.snip_img_display import SnipImgDisplayBox
from app.views.widgets.button import ButtonBox
from app.views.widgets.latex_display import LatexDisplayBox
from app.views.widgets.latex_edit import LatexEditBox
from app.views.widgets.status import StatusBar
from app.views.widgets.tray import Tray
from app.utils.global_hot_key import GlobalHotkeyManager

class MainWindow(QMainWindow):
    def __init__(self, config, title="Latex公式截图OCR"):
        super().__init__()
        # INFO: 配置文件
        self.config = config
        # INFO: 声明在主窗口中即将会用到的各个组件
        self.menu_bar = MenuBar(self) # 菜单栏
        self.snip_img_display_box = SnipImgDisplayBox() # 截图的展示组件
        self.button_box = ButtonBox(self) # 按键的组件
        self.latex_display_box = LatexDisplayBox() # 结果的展示组件
        self.latex_edit_box = LatexEditBox() # 可编辑的latex
        self.status_bar = StatusBar() # 状态栏
        self.tray = Tray(self) # 托盘
        self.setStatusBar(self.status_bar.get_status()) # 状态栏

        # INFO: 全局热键
        self.hotkey_manager = GlobalHotkeyManager()

        self.__set_main_window_ui(title=title)
        self.show()

    def __set_main_window_ui(self, title):
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon(':/icons/icon.svg'))
        self.setGeometry(300, 300, 500, 300)
        # INFO: 设置初始大小
        self.resize(800, 400)

        # INFO: 布局
        central_widget = QWidget()
        central_widget.setMinimumWidth(200)
        self.setCentralWidget(central_widget)

        lay = QVBoxLayout(central_widget)
        lay.addWidget(self.snip_img_display_box, stretch=6) # 截图展示
        lay.addWidget(self.button_box) # 按钮
        lay.addWidget(self.latex_display_box, stretch=4)
        lay.addWidget(self.latex_edit_box, stretch=2)
        

    # INFO: 重写关闭事件
    def closeEvent(self, event):
        close_flag = self.config.config.get('UI', 'close_flag', fallback="close")
        if close_flag == "close":
            self.hotkey_manager.stop()
            event.accept()
            QApplication.quit()
        else:
            event.ignore()  # 阻止默认关闭行为
            self.hide()  # 隐藏主窗口
            self.tray.tray_icon.setVisible(True)  # 显示托盘图标