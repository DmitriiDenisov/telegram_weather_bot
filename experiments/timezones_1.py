# https://stackoverflow.com/questions/15692906/python-datetime-tzinfo-time-zone-names-documentation
import datetime
import pytz
import datetime as DT

eastern = pytz.timezone('US/Eastern')
utc = pytz.utc
test = '2013-03-27 23:05'

test2 = DT.datetime.strptime(test, '%Y-%m-%d %H:%M')
print(test2)
# 2013-03-27 23:05:00

print(eastern.localize(test2))
# 2013-03-27 23:05:00-04:00

print(utc.localize(test2))
# 2013-03-27 23:05:00+00:00

test2_eastern = eastern.localize(test2)
print(test2_eastern.astimezone(utc))
# 2013-03-28 03:05:00+00:00


timezones = pytz.all_timezones
print(timezones)

from datetime import datetime, time

t = time(13, 56)
q = datetime.combine(datetime.today(), t).astimezone(pytz.utc).time()
# t = datetime.time(10, 58, 00, 000000).astimezone(pytz.utc)
print(t.tzinfo)
print(q.tzinfo)
print(datetime.today())
print(q)

from datetime import datetime, time
import pytz

t = time(12, 56, 44, 398402)


def timetz_to_tz(t, tz_out):
    return datetime.combine(datetime.today(), t).astimezone(tz_out).timetz()


def timetz_to_tz_naive(t, tz_out):
    return datetime.combine(datetime.today(), t).astimezone(tz_out).time()


def time_to_tz(t, tz_out):
    return tz_out.localize(datetime.combine(datetime.today(), t)).timetz()


def time_to_tz_naive(t, tz_in, tz_out):
    return tz_in.localize(datetime.combine(datetime.today(), t)).astimezone(tz_out).time()


print('-----------------')
t = time(19, 5, 00, 000000)  # pytz.timezone('Asia/Dubai')
q = time_to_tz_naive(t, pytz.timezone('Asia/Dubai'), pytz.utc)
print(t)
print(q)
print(q.tzinfo)
print(t.tzinfo)
a = 3
