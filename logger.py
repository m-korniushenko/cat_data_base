import logging
import os
from datetime import datetime


class DailyRotatingFileHandler(logging.Handler):
    def __init__(self, log_dir="logs", base_filename="cats", encoding="utf-8"):
        super().__init__()
        self.log_dir = log_dir
        self.base_filename = base_filename
        self.encoding = encoding
        self.current_date = None
        self.file = None
        self.ensure_log_file()

    def ensure_log_file(self):
        today = datetime.now().strftime("%Y-%m-%d")
        if (
            self.current_date != today or 
            self.file is None or 
            self.file.closed
        ):
            if self.file and not self.file.closed:
                try:
                    self.file.close()
                except Exception as e:
                    print(f"[LogError] Failed to close log file: {e}")
            self.current_date = today
            os.makedirs(self.log_dir, exist_ok=True)
            filename = os.path.join(self.log_dir, f"{self.base_filename}_{today}.log")
            try:
                self.file = open(filename, "a", encoding=self.encoding)
            except Exception as e:
                print(f"[LogError] Failed to open log file: {e}")
                self.file = None

    def emit(self, record):
        try:
            self.ensure_log_file()
            if self.file and not self.file.closed:
                msg = self.format(record)
                self.file.write(msg + "\n")
                self.file.flush()
            else:
                print("[LogError] Cannot write log — file is not open.")
        except Exception as e:
            print(f"[LogError] Failed to write log: {e}")

    def close(self):
        if self.file and not self.file.closed:
            try:
                self.file.close()
            except Exception as e:
                print(f"[LogError] Failed to close log file during handler close: {e}")
        super().close()


logger = logging.getLogger("bot")
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

# stream_handler = logging.StreamHandler()
# stream_handler.setFormatter(formatter)

daily_file_handler = DailyRotatingFileHandler()
daily_file_handler.setFormatter(formatter)

# logger.addHandler(stream_handler)
logger.addHandler(daily_file_handler)
