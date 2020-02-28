from twitter_analyzer.analyzer import analyzer
import datetime

fun = analyzer.Analyzer.check_series_time_condition
timestamp_offset = analyzer.Analyzer.timestamp_offset
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
