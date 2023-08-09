from skyfield.api import load
from datetime import datetime
import numpy as np
import arrow

ts = load.timescale()

def get_time_from_iso(iso_str):
    return datetime.strptime(iso_str, '%Y-%m-%dT%H:%M:%SZ')

def get_time_from_std(std_str):
    return datetime.strptime(std_str, '%Y-%m-%d %H:%M:%S')

def get_iso_from_std(std_str):
    return datetime.strptime(std_str, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%dT%H:%M:%SZ')

def get_std_from_iso(iso_str):
    return datetime.strptime(iso_str, '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d %H:%M:%S')

def get_ts_from_time(dt):

    return ts.utc(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)

def get_ts_from_std(std_str):
    """得到skyfield库中的时间"""
    dt = get_time_from_std(std_str)
    return get_ts_from_time(dt)

def get_ts_from_iso(iso_str):
    # dt = get_time_from_iso(iso_str)
    # return get_ts_from_time(dt)
    t_arr = arrow.get(iso_str)
    return ts.from_datetime(t_arr)

def get_ts_array_from_std(start_std : str, end_std : str, timescale):
    start_time = get_time_from_std(start_std)
    end_time = get_time_from_std(end_std)

    np_time_array = np.arange(start_time, end_time, timescale*1000)
    ts_array = [get_ts_from_time(np_time.astype(datetime)) for np_time in np_time_array]

    return ts_array

def get_ts_array_from_iso(start_iso: str, end_iso: str, timescale):
    frame = 'second'
    if timescale >= 1000:
        timescale = timescale // 1000
    else:
        frame = 'microsecond'
        timescale = timescale * 1000

    start_arrow = arrow.get(start_iso)
    end_arrow = arrow.get(end_iso)


    ts_array = ts.from_datetimes(
        [s[0] for s in arrow.Arrow.interval(frame, start_arrow, end_arrow, timescale, exact=True)])

    return ts_array

def get_julian_from_std(std_str):
    """得到julian的JDN和分数, JD = jd + fr"""
    t_sky = get_ts_from_std(std_str)
    return t_sky.whole, t_sky.tt_fraction

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

def get_julian_from_iso(s: str):
    t_arr = arrow.get(s)
    t_sky = ts.from_datetime(t_arr)
    return t_sky.whole, t_sky.ut1_fraction;

if __name__ == "__main__":
    a = get_ts_array_from_std('2023-3-1 00:00:00', '2023-3-1 00:04:59', 1000)

    print(a)