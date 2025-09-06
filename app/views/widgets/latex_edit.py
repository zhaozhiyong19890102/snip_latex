from PySide6.QtWidgets import QGroupBox, QVBoxLayout, QTextEdit

class LatexEditBox(QGroupBox):
    def __init__(self):
        super().__init__()
        self.latex_edit = QTextEdit(self)
        self.latex_edit.setMinimumHeight(40)
        self.__init_ui()

        self.latex_edit.setStyleSheet("""
            QTextEdit:focus {
                border: 1px solid #f4645f;
            }"""
        )

    def __init_ui(self):
        self.setTitle("可编辑Latex")
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.latex_edit, stretch=2)
        self.setLayout(self.vbox)

    def set_text(self, text):
        self.latex_edit.setText(text)