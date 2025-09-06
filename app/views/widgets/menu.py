from PySide6.QtGui import QAction, QIcon

class MenuBar:
    def __init__(self, parent):
        self.parent = parent
        self.menu_bar = self.parent.menuBar()
        self.menu_bar.setNativeMenuBar(True)  # 启用系统原生样式
        # INFO: 配置信息
        self.config = self.parent.config

        self.__create_action()
        self.__init_ui()

    def __init_ui(self):
        file_menu = self.menu_bar.addMenu("&文件")
        file_menu.addAction(self.new_snip_action)
        file_menu.addAction(self.preference_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        edit_menu = self.menu_bar.addMenu("&编辑")
        edit_menu.addAction(self.model_info_action)

        help_menu = self.menu_bar.addMenu("&帮助")
        help_menu.addAction(self.about_action)

        self.menu_bar.setStyleSheet(
            """
            QMenuBar::item:selected {background: #f4645f;}
            QMenu::item:selected {background: #f4645f;}
            """)

    def __create_action(self):
        # INFO: 新建截图
        self.new_snip_action = QAction(QIcon(':/icons/icon.svg'), "&新建")
        # INFO: 设置
        self.preference_action = QAction(QIcon(':/icons/preference.svg'), "&设置")
        # INFO: 退出
        self.exit_action = QAction(QIcon(":/icons/close.svg"), "&关闭")
        # INFO: 模型信息
        self.model_info_action = QAction(QIcon(":/icons/info.svg"), "&模型")
        # INFO: 关于
        self.about_action = QAction(QIcon(":/icons/help.svg"), "&关于")