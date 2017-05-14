import time, calendar, datetime

today = time.localtime(time.time())

T = calendar.monthrange(today[0], today[1]+1)[-1]

weekend = []
friday = []
for i in range(1, T+1):
    nofday = datetime.datetime(today[0], today[1]+1, i).isoweekday()
    if nofday == 5:
        friday.append(i)
    elif nofday > 5:
        weekend.append(i)
print(weekend, friday)