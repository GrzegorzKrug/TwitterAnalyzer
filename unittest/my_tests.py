from twitter_analyzer.analyzer import analyzer
import datetime
timezone_offset = 3600

fun = analyzer.Analyzer.check_series_time_condition
timestamp_offset = analyzer.Analyzer.timestamp_offset
timestamp_from_date = analyzer.Analyzer.timestamp_from_date

series = ['Sat Feb 22 11:24:15 +0000 2020',
          'Sat Feb 26 11:24:15 +0000 2020',
          'Sat Feb 29 11:24:15 +0000 2020',
          'Sat Feb 29 12:24:15 +0000 2020']
tmps = 1582466337


def test_date():
    timestamp_min = timestamp_offset(tmps=tmps, day=-10)
    timestamp_max = timestamp_offset(tmps=tmps, day=-1)
    out = fun(series, timestamp_min, timestamp_max)
    assert out[0] is True


def test_date2():
    timestamp_min = timestamp_offset(tmps=tmps, day=-15)
    out = fun(series, timestamp_min, tmps)
    assert out[1] is False


def test_date3():
    timestamp_min = timestamp_offset(tmps=tmps, day=-1)
    timestamp_max = timestamp_offset(tmps=tmps, day=6, hour=-2)
    out = fun(series, timestamp_min, timestamp_max)
    assert out[0] is False
    assert out[1] is True
    assert out[2] is True
    assert out[3] is False


def test_timestamp_off1_min():
    out = timestamp_offset(tmps=tmps, minute=1)
    assert out == tmps + 60


def test_timestamp_off2_hour():
    out = timestamp_offset(tmps=tmps, hour=1)
    assert out == tmps + 3600


def test_timestamp_off3_day():
    out = timestamp_offset(tmps=tmps, day=1)
    assert out == tmps + 24*3600


def test_timestamp_off4_month_feb29():
    out = timestamp_offset(tmps=tmps, month=1)
    assert out == tmps + 29*24*3600


def test_timestamp_off4_month_2months():
    out = timestamp_offset(tmps=tmps, month=2)
    assert out == tmps + 29*24*3600 + 31*24*3600


def test_timestamp_off5_year():
    out = timestamp_offset(tmps=tmps, year=1)
    assert out == tmps + 366 * 24 * 3600


def test_timestamp_neg_off1_min():
    out = timestamp_offset(tmps=tmps, minute=-1)
    assert out == tmps - 60


def test_timestamp_neg_off2_hour():
    out = timestamp_offset(tmps=tmps, hour=-1)
    assert out == tmps - 3600


def test_timestamp_neg_off3_day():
    out = timestamp_offset(tmps=tmps, day=-1)
    assert out == tmps - 24*3600


def test_timestamp_neg_off4_month_feb29():
    out = timestamp_offset(tmps=tmps, month=-1)
    assert out == tmps - 31*24*3600


def test_timestamp_neg_off4_month_2months():
    out = timestamp_offset(tmps=tmps, month=-2)
    good = tmps - 31*24*3600 - 31*24*3600
    assert out == good


def test_timestamp_neg_off5_year():
    out = timestamp_offset(tmps=tmps, year=-1)
    good = tmps - 365 * 24 * 3600
    assert out == good


def test_timestamp_multi_off1():
    out = timestamp_offset(tmps=tmps, month=12)
    good = tmps + 366 * 24 * 3600
    assert out == good


def test_timestamp_multi_off2():
    out = timestamp_offset(tmps=tmps, month=24)
    good = tmps + (366 + 365)*24*3600
    assert out == good


def test_timestamp_multi_off3():
    out = timestamp_offset(tmps=tmps, year=2)
    good = tmps + (366 + 365)*24*3600
    assert out == good


def test_timestamp_multi_off4():
    out = timestamp_offset(tmps=tmps, year=-2)
    good = tmps - (365 + 365)*24*3600
    assert out == good


def test_check_local_language():
    date = 'Fri Feb 21 16:34:43 +0000 2020'
    datetime.datetime.strptime(date, '%a %b %d %X %z %Y')
    timestamp_min = timestamp_offset(day=3)
    timestamp_max = timestamp_offset(day=5)
    fun(series, timestamp_min, timestamp_max)

def test_timestamp_date():
    import calendar
    # date = '2020-02-28 14:53:38.483896'
    date = 'Thu Feb 28 14:53:38 +0000 2020'
    year = 2020
    month = 2
    day = 28
    hour = 14
    minute = 53

    good_timestamp = 1582897980 + timezone_offset
    timestamp = timestamp_from_date(year=year, month=month, day=day, hour=hour, minute=minute)
    assert  good_timestamp == timestamp

def test_timestamp_date_2():
    # 2020-02-28 15:17:38.244787
    # 1582899458.244787
    year = 2020
    month = 2
    day = 28
    hour = 0
    minute = 0
    good_timestamp = 1582899458 - 15*3600 - 17*60 - 38 + timezone_offset

    timestamp = timestamp_from_date(year=year, month=month, day=day, hour=hour, minute=minute)
    assert good_timestamp == timestamp

def test_timestamp_old():
    year = 1970
    month = 1
    day = 10
    hour = 0
    minute = 0

    dt = datetime.date(year=year, month=month, day=day)
    timestamp = timestamp_from_date(year=year, month=month, day=day, hour=hour, minute=minute)
    good = 9 * 24 * 3600
    assert timestamp == good

def test_timestamp_old_2():
    year = 1970
    month = 1
    day = 10
    hour = 0
    minute = 10

    dt = datetime.date(year=year, month=month, day=day)
    timestamp = timestamp_from_date(year=year, month=month, day=day, hour=hour, minute=minute)
    good = 9 * 24 * 3600 + 10*60
    assert timestamp == good
