from app.views.main_window import MainWindow
from app.controllers.main_window_controller import MainWindowController
from app.utils.config import Config

from sys import argv, exit
from PySide6.QtWidgets import QApplication

def main():
    # INFO: 读取配置文件
    config = Config()
    app = QApplication(argv)
    # INFO: 窗口关闭后，应用程序继续在后台运行
    # （例如后台服务或托盘应用），
    # 需手动调用 QApplication::quit()退出
    app.setQuitOnLastWindowClosed(False)
    window = MainWindow(config)
    ctrl = MainWindowController(window)
    exit(app.exec())

if __name__ == "__main__":
    main()