from configparser import ConfigParser
from platform import system
import os
from pathlib import Path

class Config:
    def __init__(self):
        self.config = ConfigParser()
        # INFO: 目录信息
        # INFO：初始化配置
        self.config_file = self.__init_config_file()

        # INFO: 加载配置文件
        self.config.read(self.config_file)
    
    def __init_config_file(self):
        if system() == "Windows":
            base_dir = Path(os.environ["LOCALAPPDATA"]) / "SnipLatex"
        elif system() == "Linux":
            base_dir = Path.home() / ".config/SnipLatex"
        else:  # macOS
            base_dir = Path.home() / "Library/Application Support/SnipLatex"

        if not base_dir.parent.exists():
            base_dir.parent.mkdir(parents=True)

        if not base_dir.exists():
            base_dir.mkdir(parents=True)
        
        # INFO: 判断文件是否存在，不存在则初始化一个文件
        config_file = os.path.join(base_dir, "config.ini")
        if not os.path.exists(config_file):
            self.__init_base_config_info(config_file)
        return config_file

    def __init_base_config_info(self, config_file):
        # INFO: 基础的配置信息
        if not self.config.has_section('UI'):
            self.config.add_section('UI')
        if not self.config.has_section("USER"):
            self.config.add_section("USER")

        self.config.set('UI', 'close_flag', "close") # close/tray

        with open(config_file, 'w') as f:
            self.config.write(f)

    def save_info(self, first, second, value):
        self.config.set(first, second, value)
        with open(self.config_file, 'w') as f:
            self.config.write(f)