from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMessageBox, QApplication
from PySide6.QtGui import QIcon
import resources.resources

from app.views.widgets.model_info import ModelInfoDialog
from app.views.widgets.preference import PreferenceDialog

class MenuController:
    def __init__(self, menu_view, main_window_view, main_controller):
        self.menu_view = menu_view
        self.main_window_view = main_window_view
        self.main_controller = main_controller

        self.model_info_dialog = ModelInfoDialog(self.menu_view.config)
        self.preference_dialog = PreferenceDialog(self.menu_view.config)

        # INFO: 新建截图
        self.menu_view.new_snip_action.triggered.connect(self.__new_snip)
        # INFO: 设置
        self.menu_view.preference_action.triggered.connect(self.__preference)
        # INFO: 关闭
        self.menu_view.exit_action.triggered.connect(self.__exit)
        # INFO: 编辑模型信息
        self.menu_view.model_info_action.triggered.connect(self.__edit_model_info)
        self.menu_view.about_action.triggered.connect(self.__about)

    @Slot()
    def __new_snip(self):
        self.main_window_view.button_box.snip_button.click()

    @Slot()
    def __preference(self):
        self.preference_dialog.exec()

    @Slot()
    def __exit(self):
        QApplication.quit()

    @Slot()
    def __edit_model_info(self):
        self.model_info_dialog.exec()

    
    @Slot()
    def __about(self):
        msg = QMessageBox()
        msg.setWindowTitle("关于 Latex公式截图OCR ")
        msg.setWindowIcon(QIcon(":/icons/info.svg"))
        msg.setStyleSheet(
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
        msg.setText("SnipLatex-V1.0.2（2025-08-24）\n"
        "- 增强识别效果\n"
        "- 增加账号的使用人数")
        msg.exec()

    def get_model_info(self):
        api_url = self.model_info_dialog.api_url_input.text()
        api_key = self.model_info_dialog.api_key_input.text()
        model = self.model_info_dialog.model_input.text()
        return (api_url, api_key, model)