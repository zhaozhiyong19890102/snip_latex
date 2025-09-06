import threading
from PySide6 import QtCore
from pynput import keyboard

class GlobalHotkeyManager(QtCore.QObject):
    activated = QtCore.Signal()
    
    def __init__(self):
        super().__init__()
        self.listener = None
        self.running = False  # 新增运行状态标志[1](@ref)
        
    def start(self):
        self.running = True
        threading.Thread(target=self._run_listener, daemon=True).start()
        
    def stop(self):
        self.running = False
        if self.listener:
            self.listener.stop()  # 确保监听器被正确停止[1,7](@ref)
    
    def _run_listener(self):
        """重构监听器逻辑，使用更可靠的GlobalHotKeys API[7](@ref)"""
        try:
            with keyboard.GlobalHotKeys({
                '<shift>+<alt>+s': self._trigger_signal  # 修正热键语法
            }) as self.listener:
                while self.running:  # 添加循环防止线程提前退出
                    QtCore.QThread.msleep(100)
        except Exception as e:
            print(f"监听器错误: {e}")
    
    def _trigger_signal(self):
        self.activated.emit()