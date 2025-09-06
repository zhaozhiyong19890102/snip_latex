from app.utils.process_signal import ProcessingSignal
from app.utils.model_thread import ModelThread

import resources.resources

from io import BytesIO
from base64 import b64encode
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QIcon
from json import loads
from PIL import Image

BASE_WIDTH = 500
BASE_HEIGHT = 70

class ButtonController:
    def __init__(self, main_window_view, button_view, main_controller):
        self.main_window_view = main_window_view
        self.button_view = button_view

        self.main_controller = main_controller

        # INFO: 截图按钮的信号
        self.button_view.snip_button.clicked.connect(self.__on_click)
        # INFO: 识别按钮的型号
        self.button_view.reco_button.clicked.connect(self.__recognition)
        # INFO: 快捷键的槽函数
        self.button_view.shortcut_snip.activated.connect(self.__on_snip_triggered)

        # INFO: 热键
        self.main_window_view.hotkey_manager.activated.connect(self.__on_snip_triggered)
        self.main_window_view.hotkey_manager.start()

        self.ocr_processing = ProcessingSignal(self)
        self.is_processing = False

    def __pil_to_base64(self, pil_img, format="PNG"):
        buffered = BytesIO()
        pil_img.save(buffered, format=format)  # 保存图像到内存缓冲区
        img_bytes = buffered.getvalue()
        return b64encode(img_bytes).decode("utf-8")  # 编码为Base64字符串

    def ret_snip(self, img=None):
        r''' 更新截图到指定位置
        '''
        if not img:
            self.main_window_view.show()
            return
        width, height = img.size
        print(f"width: {width}, height: {height}")
        if width <= 0 or height <= 0:
            self.main_window_view.show()
            return
        
        # INFO: 针对长或者宽太小，会影响到识别质量的，resize
        img_resize = img
        if width < 500:
            ratio = BASE_WIDTH / width
            new_height = int(height * ratio)
            new_size = (BASE_WIDTH, new_height)
            img_resize = img.resize(new_size, Image.LANCZOS)

        if height < 70:
            ratio = BASE_HEIGHT / height
            new_width = int(width * ratio)
            new_size = (new_width, BASE_HEIGHT)
            img_resize = img.resize(new_size, Image.LANCZOS)

        self.button_view.img = img_resize
        self.main_window_view.show()
        base64_str = self.__pil_to_base64(img_resize, "PNG")
        data_uri = f"data:image/png;base64,{base64_str}"
        img_sorce = f"""<center>
            <img src={data_uri} height="100%">
            </center>"""
        # INFO: 设置图片到对应的位置
        self.main_window_view.snip_img_display_box.set_image(img_sorce)
        # INFO: 图片返回后设置“识别”按钮可用
        self.button_view.reco_button.setEnabled(True)

    @Slot()
    def __on_click(self):
        # INFO: 关闭父窗口
        self.main_window_view.hide()
        # INFO: 开启截图窗口
        self.is_snipping = True
        self.main_controller.snip_controller.snip()

    @Slot()
    def __on_snip_triggered(self):
        self.button_view.snip_button.click()  # 模拟点击截图按钮

    @Slot()
    def __recognition(self):
        self.is_processing = True
        self.display_prediction()
        self.ocr_processing.process_status_emit(True)
        if self.button_view.img != None:
            api_url, api_key, model = self.main_controller.menu_controller.get_model_info()
            if api_url == "" or api_key == "" or model == "":
                self.ocr_processing.process_status_emit(False)
                msg = QMessageBox()
                msg.setWindowTitle(" ")
                msg.setWindowIcon(QIcon(":/icons/error.svg"))
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
                msg.setText("请先在“编辑”中设置“API-URL”和“API-KEY”")
                msg.exec()
            else:
                self.thread = ModelThread(self.button_view.img, api_url, api_key, model)
                self.thread.finished.connect(self.__ret_prediction)
                # INFO: 完成后自动销毁线程
                self.thread.finished.connect(self.thread.deleteLater)
                self.thread.start()
        else:
            self.ocr_processing.process_status_emit(False)
            msg = QMessageBox()
            msg.setWindowTitle(" ")
            msg.setWindowIcon(QIcon(":/icons/error.svg"))
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
            msg.setText("没有图片")
            msg.exec()

    @Slot()
    def __ret_prediction(self, result):
        self.is_processing = False
        success, prediction = result["success"], result["prediction"]

        if success:
            self.ocr_processing.process_status_emit(False, prediction)
            # INFO: 结果的解析
            fianl_ans = loads(prediction)
            print(f"prediction: {prediction}")
            if fianl_ans["formula"] == "no":
                self.ocr_processing.process_status_emit(False)
                msg = QMessageBox()
                msg.setWindowTitle(" ")
                msg.setWindowIcon(QIcon(":/icons/error.svg"))
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
                msg.setText("请输入正确的包含公式的图片")
                msg.exec()
            else:
                prediction_content = fianl_ans["content"]
                print(f"prediction_content: {prediction_content}")
                self.display_prediction(prediction_content)
                self.main_window_view.latex_edit_box.set_text(prediction_content)
        else:
            self.ocr_processing.process_status_emit(False)
            msg = QMessageBox()
            msg.setWindowTitle(" ")
            msg.setWindowIcon(QIcon(":/icons/error.svg"))
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
            msg.setText(prediction)
            msg.exec()

    def display_prediction(self, prediction=None):
        if self.is_processing:
            pageSource = """<center>
            <img src="qrc:/icons/processing-icon-anim.svg" width="50", height="50">
            </center>"""
        else:
            # if prediction is None:
            #     prediction = self.textbox.toPlainText().strip('$')
            pageSource = """
            <html>
            <head><script id="MathJax-script" src="qrc:MathJax.js"></script>
            <script>
            MathJax.Hub.Config({messageStyle: 'none',tex2jax: {preview: 'none'}});
            MathJax.Hub.Queue(
                function () {
                    document.getElementById("equation").style.visibility = "";
                }
                );
            </script>
            </head> """ + """
            <body>
            <div id="equation" style="font-size:1em; visibility:hidden">$${equation}$$</div>
            </body>
            </html>
                """.format(equation=prediction)
        self.main_window_view.latex_display_box.set_latex(pageSource)