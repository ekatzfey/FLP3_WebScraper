import time
import datetime

def datestr( d ):
    return str(d.month).zfill(2) + '/' + \
        str(d.day).zfill(2) + '/' + \
        str(d.year)

start_date = datetime.date(2016, 2, 13)

print datestr(start_date)

end_date = start_date + datetime.timedelta(days=7)

print datestr(end_date)
