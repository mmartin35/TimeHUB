from datetime import time
from .data import convert_time_to_hours_from_midnight
            
def fetch_daysoff(day_gap: int, x: int, y: int, rnd: int, ratio: int):
    return (round(day_gap * (x / y), rnd) * ratio / 100)

def calculate_worktime(t1: time, t2: time, t3: time, t4: time):
    return (convert_time_to_hours_from_midnight(t2) - convert_time_to_hours_from_midnight(t1) + convert_time_to_hours_from_midnight(t4) - convert_time_to_hours_from_midnight(t3))
