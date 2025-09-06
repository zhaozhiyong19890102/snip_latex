from PySide6.QtWidgets import QGroupBox, QVBoxLayout
from PySide6.QtWebEngineWidgets import QWebEngineView

class SnipImgDisplay(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(120)

class SnipImgDisplayBox(QGroupBox):
    def __init__(self):
        super().__init__()
        self.img_display = SnipImgDisplay()
        self.__set_img_display_ui()

    def __set_img_display_ui(self):
        self.setTitle("截图")
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.img_display, stretch=4)
        self.setLayout(self.vbox)

    def set_image(self, html=""):
        self.img_display.setHtml(html)