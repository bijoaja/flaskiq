import time
from datetime import datetime, timedelta, date

class Duration:
    def __init__(self):
        self.start_time = None
        self.timestamp_start = None

    def start(self):
        """Mulai pengukuran waktu dan simpan timestamp awal"""
        self.start_time = time.time()

    def get_timestamp(self):
        """Ambil timestamp awal proses (format readable)"""
        self.timestamp_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return self.timestamp_start

    def get_duration(self):
        """Hitung durasi sejak waktu start"""
        if self.start_time is None:
            return 0
        return round(time.time() - self.start_time, 4)
