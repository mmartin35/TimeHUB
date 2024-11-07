from pointer.models import DailyTimer
from datetime import datetime, timedelta
from .data import convert_time_to_hours_from_midnight
            
def fetch_daysoff(day_gap, x, y, rnd, ratio):
    return (round(day_gap * (x / y), rnd) * ratio / 100)

def calculate_worktime(t1, t2, t3, t4):
    return (convert_time_to_hours_from_midnight(t2) - convert_time_to_hours_from_midnight(t1) + convert_time_to_hours_from_midnight(t4) - convert_time_to_hours_from_midnight(t3))