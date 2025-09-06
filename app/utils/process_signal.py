from PySide6.QtCore import QObject, Signal

class ProcessingSignal(QObject):
    ocr_processing = Signal(dict)

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.ocr_processing.connect(self.__process_status)

    def process_status_emit(self, process_status, prediction=None):
        self.ocr_processing.emit({"process_status": process_status, "prediction": prediction})

    def __process_status(self, status):
        ocr_processing_flag, prediction = status["process_status"], status["prediction"]
        print(f"ocr_processing_flag: {ocr_processing_flag}")
        if ocr_processing_flag:
            self.parent.is_processing = True
            self.parent.button_view.snip_button.setEnabled(False)
        else:
            self.parent.is_processing = False
            self.parent.button_view.snip_button.setEnabled(True)
            self.parent.display_prediction(prediction)