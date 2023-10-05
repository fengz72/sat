import sys
sys.path.extend(['../..'])

import arrow
import numpy as np
from skyfield.api import load
from sat.obj.gs import GroundStation
from sat.tool.sat_tools import auto_get_sat_dict
from sat.tool.gs_tools import auto_get_gs_list


start = arrow.get('2023-9-1T00:00:00')
end = arrow.get('2023-9-1T01:30:00')

def f():
    ts = load.timescale()
    sats = auto_get_sat_dict('../test.yaml')
    gs = auto_get_gs_list(sats, '../test.yaml')

    for g in gs:
        print(g.name)
        t_arr = arrow.Arrow.interval('minute', start, end, 1, exact=True)
        pre_sat = ""
        for t in t_arr:
            t_sky = ts.from_datetime(t[0])
            link_sat = g.get_link_sat(t_sky)
            if link_sat[1] != pre_sat:
                print(link_sat[1], t[0])
                pre_sat = link_sat[1]


def link(n, error, gs_num):
    fs = open('log.txt', 'a')

    sats = auto_get_sat_dict('../conf.yaml')
    source = []
    dest = []
    for i in range(0, gs_num):
        tmp = gen_gs("source" + str(i), 60, 180, 0, 40, sats)
        source.append(tmp)
        tmp = gen_gs("dest" + str(i), 60, 180, 0, 40, sats)
        dest.append(tmp)

    ts = load.timescale()
    t_arr = arrow.Arrow.interval('minute', start, end, 1, exact=True)

    count = 0
    res = [0] * (n + 1)
    for t in t_arr:
        count += 1
        t_sky = ts.from_datetime(t[0])
        for g in dest:
            link_sat_source = g.shortest_link_sat(t_sky)
            link_sat_dest = g.shortest_link_sat_random(t_sky, error, link_sat_source)
            man_dis = manhattan_distance(link_sat_dest, link_sat_source)
            for i in range(0, n + 1):
                if man_dis <= i:
                    res[i] += 1
            # print("理想: " + link_sat_source + ", 实际: " + link_sat_dest)
    total = count * len(dest)
    print("total: " + str(total) + ", error: " + str(error), file=fs)
    print(res, file=fs)

    fs.close()


def gen_gs(name, lat_range, lon_range, height, degree, sats):
    lat = np.random.uniform(-lat_range, lat_range)
    lon = np.random.uniform(-lon_range, lon_range)

    return GroundStation(name, lat, lon, height, degree, sats)

def manhattan_distance(sat1, sat2):
    arr1 = sat1.split("_")
    p1 = int(arr1[0])
    n1 = int(arr1[1])

    arr2 = sat2.split("_")
    p2 = int(arr2[0])
    n2 = int(arr2[1])

    return abs(p1 - p2) + abs(n1 - n2)

if __name__ == '__main__':

    print("start!")
    # f()
    for i in range(2, 11, 2):
        link(5, i, 100)

    # for i in range(2, 6, 2):
    #     link(5, i, 5)

    print("done!")