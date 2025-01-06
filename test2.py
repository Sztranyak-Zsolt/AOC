import datetime
from typing import Callable


def DM_execution_dt_trigger(execution_date):
    if execution_date.strftime('%A') == "Friday":
        return execution_date + datetime.timedelta(days=2)
    return execution_date


print(DM_execution_dt_trigger(datetime.datetime.now() - datetime.timedelta(days=3)))

print(isinstance(DM_execution_dt_trigger, Callable))
