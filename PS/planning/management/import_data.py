import os
from django.conf import settings
from pointer.models import DailyTimer
import pandas as pd

def import_data():
    path = os.path.join(settings.BASE_DIR, 'planning/management/test.ods')
    wb = pd.read_excel(path, 'Sheet1', engine='odf')

    print("Importing data")
    df = pd.DataFrame(wb)
    for index, row in df.iterrows():
        try:
            DailyTimer.objects.create(
                intern_id=row['intern_id'],
                date=row['date'],
                t1=row['t1'],
                t2=row['t2'],
                t3=row['t3'],
                t4=row['t4'],
                worktime=row['worktime'],
            )
            print(f"Imported row {index}")
        except Exception as e:
            print(f"Error importing row {index}: {e}")