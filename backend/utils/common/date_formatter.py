__author__ = 'parkjiminy'

import datetime
import traceback
import logging
import time

logger = logging.getLogger(__name__)

def facebook_date_to_timestamp(fb_date):
	if fb_date == '0' or fb_date == 0 or fb_date == None:
		return 0
	elif str(fb_date).find("T") > -1 and str(fb_date).find("-0700") > -1 :
		dt1 = datetime.datetime.strptime(fb_date, '%Y-%m-%dT%H:%M:%S-0700')
		dt1_timestamp = dt1.timestamp()
		return int(dt1_timestamp)
	elif str(fb_date).find("T") > -1 and str(fb_date).find("-0800") > -1 :
		dt1 = datetime.datetime.strptime(fb_date, '%Y-%m-%dT%H:%M:%S-0800')
		dt1_timestamp = dt1.timestamp()
		return int(dt1_timestamp)
	elif str(fb_date).find("T") > -1 and str(fb_date).find("+0900") > -1 :
		dt1 = datetime.datetime.strptime(fb_date, '%Y-%m-%dT%H:%M:%S+0900')
		dt1_timestamp = dt1.timestamp()
		return int(dt1_timestamp)
	elif str(fb_date).find("T") > -1 and str(fb_date).find("+0000") > -1 :
		dt1 = datetime.datetime.strptime(fb_date, '%Y-%m-%dT%H:%M:%S+0000')
		dt1_timestamp = dt1.timestamp()
		return int(dt1_timestamp)
	elif str(fb_date).find("T") > -1 :
		dt1 = datetime.datetime.strptime(fb_date, '%Y-%m-%dT%H:%M:%S')
		dt1_timestamp = dt1.timestamp()
		return int(dt1_timestamp)
	else :
		return fb_date

def facebook_date_to_formatted_YYYY_MM_DD_HH_MM_SS(fb_date):
	if fb_date == '0' or fb_date == 0 or fb_date == None:
		return 0
	elif str(fb_date).find("T") > -1 and str(fb_date).find("-0700") > -1 :
		dt1 = datetime.datetime.strptime(fb_date, '%Y-%m-%dT%H:%M:%S-0700')
		dt1_timestamp = dt1.timestamp()
		return datetime.datetime.fromtimestamp(int(dt1_timestamp)).strftime('%Y-%m-%d %H:%M:%S')
	elif str(fb_date).find("T") > -1 and str(fb_date).find("-0800") > -1 :
		dt1 = datetime.datetime.strptime(fb_date, '%Y-%m-%dT%H:%M:%S-0800')
		dt1_timestamp = dt1.timestamp()
		return datetime.datetime.fromtimestamp(int(dt1_timestamp)).strftime('%Y-%m-%d %H:%M:%S')
	elif str(fb_date).find("T") > -1 and str(fb_date).find("+0900") > -1 :
		dt1 = datetime.datetime.strptime(fb_date, '%Y-%m-%dT%H:%M:%S+0900')
		dt1_timestamp = dt1.timestamp()
		return datetime.datetime.fromtimestamp(int(dt1_timestamp)).strftime('%Y-%m-%d %H:%M:%S')
	elif str(fb_date).find("T") > -1 and str(fb_date).find("+0000") > -1 :
		dt1 = datetime.datetime.strptime(fb_date, '%Y-%m-%dT%H:%M:%S+0000')
		dt1_timestamp = dt1.timestamp()
		return datetime.datetime.fromtimestamp(int(dt1_timestamp)).strftime('%Y-%m-%d %H:%M:%S')
	elif str(fb_date).find("T") > -1 :
		dt1 = datetime.datetime.strptime(fb_date, '%Y-%m-%dT%H:%M:%S')
		dt1_timestamp = dt1.timestamp()
		return datetime.datetime.fromtimestamp(int(dt1_timestamp)).strftime('%Y-%m-%d %H:%M:%S')
	else :
		return fb_date

def str_to_datetime(str, format_str='%Y-%m-%d'):
	if str == None or '' or 0:
		return None
	else:
		return datetime.datetime.strptime(str, format_str)

def timestamp_to_fommated_date(stamp, format_str):
	if (stamp == '0' or stamp == 0):
		return None

	else:
		return datetime.datetime.fromtimestamp(stamp).strftime(format_str)

def timestamp_to_formatted_YYYY_MM_DD(stamp):
	if (stamp == '0' or stamp == 0):
		return None
	else:
		return datetime.datetime.fromtimestamp(stamp).strftime('%Y-%m-%d')

def datetime_to_formatted_YYYY_MM_DD(datetime):
	if datetime == '' or datetime == 0:
		return 0
	else:
		return datetime.strftime('%Y-%m-%d')

def datetime_to_formatted_YYYY_MM_DD_HH_MM_SS(datetime):
	if datetime == '' or datetime == 0:
		return 0
	else:
		return datetime.strftime('%Y-%m-%d %H:%M:%S')


def timestamp_to_formatted_YYYY_MM_DD_HH_MM_SS(stamp):
	if (stamp == '0' or stamp == 0):
		return None
	else:
		return datetime.datetime.fromtimestamp(stamp).strftime('%Y-%m-%d %H:%M:%S')

def datetime_to_timestamp(params):
	try:
		date_str = params.get('date_str', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		format_str = params.get('format_str', '%Y-%m-%d %H:%M:%S')

		temptime = datetime.datetime.strptime(date_str, format_str)
		return time.mktime(temptime.timetuple())

	except Exception:
		print(traceback.format_exc())
		logger.error(traceback.format_exc())
		return None

def perdelta(start, end, delta):
	curr = start
	while curr < end:
		yield curr
		curr += delta

def date_now():
	return datetime.datetime.now().strftime('%Y-%m-%d')

def date_cal(timedelta=0):
	time = datetime.datetime.now()
	if timedelta > 0:
		time = time + datetime.timedelta(days=timedelta)
	if timedelta < 0:
		time = time - datetime.timedelta(days=abs(timedelta))

	return time.strftime('%Y-%m-%d')

def timestamp_now():
	ts = int(time.time())
	return ts

def last_day_of_month(date):
    if date.month == 12:
        return date.replace(day=31)
    return date.replace(month=date.month+1, day=1) - datetime.timedelta(days=1)

def datediff_min(date_start, date_stop, format='%Y-%m-%d'):
	a = datetime.datetime.strptime(date_start, format)
	b = datetime.datetime.strptime(date_stop, format)

	delta = b - a

	return delta.total_seconds()

def datediff(date_start, date_stop, format='%Y-%m-%d'):
	a = datetime.datetime.strptime(date_start, format)
	b = datetime.datetime.strptime(date_stop, format)

	delta = b - a

	return delta.days

def caldate(day, format='%Y-%m-%d'):
	import time
	from datetime import date
	today = date.today()

	calday = date.fromtimestamp(time.time() - 60*60*24*day)

	return calday.strftime(format)