import pytest
from twitter_analyzer.analyzer import analyzer

fun = analyzer.Analyzer.read_time_condition
series = ['Sat Feb 22 11:24:15 +0000 2020',
          'Sat Feb 26 11:24:15 +0000 2020',
          'Sat Feb 29 11:24:15 +0000 2020']


def test_date():
    out = fun(series, 20200222112415, 20200228112415)
    assert  out[0] == True

def test_date2():
    out = fun(series, 20200220112415, 20200225112415)
    assert  out[1] == False

def test_date3():
    out = fun(series, 20200225112415, 20200229112415)
    assert  out[0] == False
    assert  out[1] == True
    assert  out[2] == True


