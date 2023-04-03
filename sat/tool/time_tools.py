from skyfield.api import load
from datetime import datetime
import numpy as np

epochTimeStr = '2023-2-24 11:30:00'  # 输入仿真的时间格式

def get_time_from_iso(iso_str):
    return datetime.strptime(iso_str, '%Y-%m-%dT%H:%M:%SZ')

def get_time_from_std(std_str):
    return datetime.strptime(std_str, '%Y-%m-%d %H:%M:%S')

def get_ts_from_time(dt):
    ts = load.timescale()
    return ts.utc(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)

def get_ts_from_std(std_str):
    """得到skyfield库中的时间"""
    dt = get_time_from_std(std_str)
    return get_ts_from_time(dt)

def get_ts_from_iso(iso_str):
    dt = get_time_from_iso(iso_str)
    return get_ts_from_time(dt)

def get_ts_array_from_std(start_std : str, end_std : str, timescale):
    start_time = get_time_from_std(start_std)
    end_time = get_time_from_std(end_std)

    np_time_array = np.arange(start_time, end_time, timescale*1000)
    ts_array = [get_ts_from_time(np_time.astype(datetime)) for np_time in np_time_array]

    return ts_array


def get_julian_from_std(std_str):
    """得到julian的JDN和分数, JD = jd + fr"""
    ts = get_ts_from_std(std_str)
    return ts.whole, ts.tt_fraction

def get_julian_from_time(date_time):
    """
    得到julian时间
    :param date_time:
    :return: jd, fr
    """
    t = get_ts_from_time(date_time)
    jd = t.whole
    fr = t.tt_fraction
    return jd, fr

if __name__ == "__main__":
    a = get_ts_array_from_std('2023-3-1 00:00:00', '2023-3-1 00:04:59', 1000)
    print(a)