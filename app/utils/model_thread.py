from app.utils.ocr_model import OCRModel

from PySide6.QtCore import QThread, Signal

class ModelThread(QThread):
    finished = Signal(dict)

    def __init__(self, img, api_url, api_key, model_name):
        super().__init__()
        self.img = img
        self.model = OCRModel(api_url, api_key, model_name)

    def run(self):
        try:
            status, message, prediction = self.model.predict(self.img)
            # INFO: 判断是否成功
            if status == 0:
                self.finished.emit({"success": True, "prediction": prediction})
            else:
                if message == None:
                    message = "预测失败"
                self.finished.emit({"success": False, "prediction": message})
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.finished.emit({"success": False, "prediction": None})