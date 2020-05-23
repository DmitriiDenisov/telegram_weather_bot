# https://stackoverflow.com/questions/7065164/how-to-make-an-unaware-datetime-timezone-aware-in-python

import datetime
import pytz

unaware = datetime.time(10, 58, 00, 000000)
aware = datetime.time(10, 58, 00, 000000, pytz.timezone('Europe/Berlin'))

now_aware = pytz.utc.localize(unaware)

print(unaware.tzinfo)
print(aware.tzinfo)

print(unaware)
print(aware)
