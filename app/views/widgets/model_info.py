from PySide6.QtWidgets import (QDialog, QLabel, QLineEdit, 
    QPushButton, QCheckBox, QGridLayout, QMessageBox, QSizePolicy
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSettings, Slot

class ModelInfoDialog(QDialog):
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.setWindowTitle("模型信息")
        self.setWindowIcon(QIcon(":/icons/info.svg"))
        self.setMinimumSize(300, 200)

        # INFO: 配置文件
        self.config = config
        
        # 创建控件
        self.api_url_label = QLabel("API_URL :")
        self.api_url_input = QLineEdit()
        
        self.api_key_label = QLabel("API-KEY :")
        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.Password)

        self.model_label = QLabel("model :")
        self.model_input = QLineEdit()
        
        self.remember_check = QCheckBox("记住 API-URL, API-KEY 和 Model")
        self.ok_button = QPushButton("确定")
        self.cancel_button = QPushButton("取消")
        
        # 布局管理
        layout = QGridLayout()
        layout.addWidget(self.api_url_label, 0, 0)
        layout.addWidget(self.api_url_input, 0, 1)
        layout.addWidget(self.api_key_label, 1, 0)
        layout.addWidget(self.api_key_input, 1, 1)
        layout.addWidget(self.model_label, 2, 0)
        layout.addWidget(self.model_input, 2, 1)
        layout.addWidget(self.remember_check, 3, 0, 1, 2)
        layout.addWidget(self.ok_button, 4, 0)
        layout.addWidget(self.cancel_button, 4, 1)
        self.setLayout(layout)
        
        # 连接信号
        self.ok_button.clicked.connect(self.authenticate)
        self.cancel_button.clicked.connect(self.reject)

        self.ok_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.cancel_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # INFO: 加载保存的凭证
        self.load_credentials()

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
        self.api_url_input.setStyleSheet("""
            QLineEdit:focus {
                border: 1px solid #f4645f;
            }"""
        )

        self.api_key_input.setStyleSheet("""
            QLineEdit:focus {
                border: 1px solid #f4645f;
            }"""
        )

    def load_credentials(self):
        """读取保存的模型信息"""
        remember = self.config.config.get('USER', 'remember', fallback="False")
        
        if remember == "True":
            self.remember_check.setChecked(True)
            api_url = self.config.config.get('USER', 'api_url', fallback="")
            api_key =  self.config.config.get('USER', 'api_key', fallback="")
            model = self.config.config.get('USER', 'model', fallback="")
            self.api_url_input.setText(api_url)
            self.api_key_input.setText(api_key)
            self.model_input.setText(model)

    def save_credentials(self):
        """保存模型信息"""
        if self.remember_check.isChecked():
            # INFO: 保存
            self.config.save_info('USER', 'remember', "True")

            self.config.save_info('USER', 'api_url', self.api_url_input.text())
            self.config.save_info('USER', 'api_key', self.api_key_input.text())
            self.config.save_info('USER', 'model', self.model_input.text())
        else:
            # INFO: 清除保存的凭证
            self.config.save_info('USER', 'remember', "False") # True/False
            self.config.save_info('USER', 'api_url', "")
            self.config.save_info('USER', 'api_key', "")
            self.config.save_info('USER', 'model', "")
            
    @Slot()
    def authenticate(self):     
        self.save_credentials()
        self.accept()  # 关闭对话框并返回Accepted[2,3](@ref)