from datetime import datetime
from pytz import timezone


class Time:
    def get_current_time(self):
        format = "%Y-%m-%d %H:%M:%S"
        # Current time in UTC
        now_utc = datetime.now(timezone('UTC'))
        # Convert to Asia/Ho_Chi_Minh time zone
        now_vn = now_utc.astimezone(timezone('Asia/Ho_Chi_Minh'))
        return now_vn.strftime(format)
