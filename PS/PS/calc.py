from pointer.models import DailyTimer
from datetime import datetime, timedelta
            
def fetch_daysoff(day_gap, x, y, rnd, ratio):
    return (round(day_gap * (x / y), rnd) * ratio / 100)

def add():
    return