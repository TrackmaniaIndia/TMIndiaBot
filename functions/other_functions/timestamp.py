from datetime import datetime

def curr_time():
    return datetime.now(timezone(timedelta(hours=5, minutes=30)))