from PySide6.QtWidgets import QStatusBar

class StatusBar():
    def __init__(self):
        self.statusBar = QStatusBar()
        self.statusBar.setStyleSheet("""
                                     QStatusBar {
                                     border: none;
                                     background-color: #f4645f;
                                     }""")
        self.statusBar.showMessage("SnipLatex-V1.0.2", 0)

    def get_status(self):
        return self.statusBar