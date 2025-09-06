from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QGroupBox, QVBoxLayout

class LatexDisplay(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(80)

class LatexDisplayBox(QGroupBox):
    def __init__(self):
        super().__init__()
        self.latexdisplay = LatexDisplay()
        self.__init_ui()

    def __init_ui(self):
        self.setTitle("识别结果")
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.latexdisplay, stretch=4)
        self.setLayout(self.vbox)

    def set_latex(self, html=""):
        self.latexdisplay.setHtml(html)
        