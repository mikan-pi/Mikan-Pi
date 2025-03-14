import logging
from collections import deque
import sys

class MainLogger(logging.Logger):
    _instance = None

    def __new__(cls, name="MainLogger", *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, name="MainLogger"):
        if not hasattr(self, "_initialized"):
            super().__init__(name)
            self.log = deque(maxlen=10)
            self._initialized = True

            # ハンドラー設定
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            self.addHandler(handler)
            self.setLevel(logging.INFO)

    def log_message(self, level, message):
        """メッセージを記録し、標準出力にも出力"""
        self.log.append(message)
        self.log(level, message)

    def get_logs(self):
        """記録されたログを取得"""
        return self.log