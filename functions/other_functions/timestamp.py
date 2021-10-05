from datetime import datetime, timezone, timedelta

def curr_time():
    return datetime.now(timezone(timedelta(hours=5, minutes=30)))