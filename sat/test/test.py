import itertools
import os.path
import random
import time

import networkx
import skyfield.api
from sgp4.api import jday, SatrecArray
from skyfield.api import EarthSatellite, load
import numpy as np
from sat.tool.distance_tools import get_distance_between_two_sat
from sat.tool.file_tools import get_yaml
from sat.tool.gs_tools import auto_get_gs_list
from sat.tool.sat_tools import auto_get_sat_dict
import math


def test():
    # 得到skyfield的time对象
    ts = load.timescale()
    t = ts.now()
    # ts.utc(2022, 10, 24, 16, 46, 10)

    # stations_url = 'http://celestrak.com/NORAD/elements/stations.txt'
    stations_url = 'https://celestrak.org/NORAD/elements/gp.php?GROUP=starlink&FORMAT=tle'
    groupName = 'starlink-all'  # 星座名称
    epochTimeStr = '2023-2-24 11:30:00'  # 输入仿真的时间格式

    now = int(time.time())
    timeArr = time.localtime(now)
    timeStr = time.strftime("%Y-%m-%d_%H-%M-%S", )

    tleFileName = './data/' + timeStr + '_' + groupName + ".txt"
    print(tleFileName)
    satellites = load.tle_file(stations_url, filename=tleFileName)  # list<EarthSatellite>

    # by_name = {sat.name for sat in satellites}
    # satellite = by_name

    oneSat = satellites[0]
    geocentric = oneSat.at(t)


def get_position_on_teme(sat_dict, start_time, end_time, timescale):
    sat_dict.values()
    ts = load.timescale()
    ts.linspace()


def test_networkx():
    ts = load.timescale()
    line1 = '1 00001U 00000ABC 23060.00080074  .00000000  00000-0  00000+0 0    03'
    line2 = '2 00001  53.0000   5.0000 0001000  90.0000  26.5909 15.06000000    09'
    sat1 = EarthSatellite(line1, line2, 'sat1', ts)
    line1 = '1 00002U 00000ABC 23060.00080074  .00000000  00000-0  00000+0 0    04'
    line2 = '2 00002  53.0000   5.0000 0001000  90.0000  53.1818 15.06000000    05'
    sat2 = EarthSatellite(line1, line2, 'sat2', ts)
    t = ts.now()
    distance = np.linalg.norm(sat1.at(t).itrf_xyz().km - sat2.at(t).itrf_xyz().km)
    sat_dict = {}
    sat_dict[sat1.name] = sat1
    sat_dict[sat2.name] = sat2

    G = nx.Graph()
    G.add_nodes_from(sat_dict.values())
    # G.add_edge(sat1, sat2, weight=distance)
    #
    # distance = np.linalg.norm(sat2.at(t).itrf_xyz().km - sat1.at(t).itrf_xyz().km)
    # G.add_edge(sat2, sat1, weight=distance)

    G.remove_node(sat1)
    print(G.nodes)


from sat.obj.sat import Satellite
from sgp4.api import Satrec, WGS72


def test_sat():
    ts = load.timescale()
    satrec = Satrec()
    satrec.sgp4init(
        WGS72,  # gravity model
        'i',  # 'a' = old AFSPC mode, 'i' = improved mode
        5,  # satnum: Satellite number
        18441.785,  # epoch: days since 1949 December 31 00:00 UT
        2.8098e-05,  # bstar: drag coefficient (/earth radii)
        6.969196665e-13,  # ndot: ballistic coefficient (revs/day)
        0.0,  # nddot: second derivative of mean motion (revs/day^3)
        0.1859667,  # ecco: eccentricity
        5.7904160274885,  # argpo: argument of perigee (radians)
        0.5980929187319,  # inclo: inclination (radians)
        0.3373093125574,  # mo: mean anomaly (radians)
        0.0472294454407,  # no_kozai: mean motion (radians/minute)
        6.0863854713832,  # nodeo: right ascension of ascending node (radians)
    )
    sat = EarthSatellite.from_satrec(satrec, ts)
    mysat = Satellite('1_1', satrec, sat, 72, 22)
    print(mysat.name)


from skyfield.api import Angle


def test_0():
    with open('../tool/gs.txt', 'r', encoding='utf-8') as f:
        list = f.readlines()
        lat = list[0].split(' ')[2]
        lon = list[0].split(' ')[3]
        height = list[0].split(' ')[4]
        print(Angle(lat, lon, 4))


def test_sort():
    link_sat = {'3_3': 20, '2_2': 80, '1_1': 1}
    # 排序
    # sorted_list = sorted(link_sat.items(), key=operator.itemgetter(1))
    # print(sorted_list)
    # 得到最小值
    # min_dis = min(link_sat, key=lambda k: link_sat[k])
    # print(min_dis)

    # 使用zip, 最小值和排序
    min_dis = min(zip(link_sat.values(), link_sat.keys()))
    print(min_dis[0])
    print(min_dis[1])
    sat_sorted = sorted(zip(link_sat.values(), link_sat.keys()))
    print(sat_sorted)


import json
import networkx as nx


def test_json():
    sat_dict = auto_get_sat_dict('../tool/conf.yaml')
    gs_list = auto_get_gs_list(sat_dict, '../tool/gs.txt')

    ts = load.timescale()
    t = ts.utc(2023, 3, 1, 1, 0, 0)
    print(type(t))

    time_str = t.tt_strftime('%Y-%m-%dT%H:%M:%SZ')
    data = {
        "time": time_str,
        # "sat": [{sat.name: [sat.get_blh(t)[0].degrees, sat.get_blh(t)[1].degrees, sat.get_blh(t)[2].m]} for sat in sat_dict.values()],
        "sat": [{'name': sat.name, 'pos': list(sat.get_xyz(t) * 1000)} for sat in sat_dict.values()],
        "gs": [{'name': gs.name, 'pos': list(gs.get_xyz())} for gs in gs_list],
        "link": [],
        "path": [],
        "dis": 0,
        "satNum": 0
    }

    G = nx.Graph()
    G.add_nodes_from(sat_dict.values())
    G.add_nodes_from(gs_list)

    print("开始计算卫星间链路~~~~~~~~~~~~~~~~~~~~~~~~")
    for sat in sat_dict.values():
        forward, back = sat.get_intra_sats(t)
        if forward is not None and back is not None:
            data["link"].append([sat.name, forward])
            data["link"].append([sat.name, back])
            forward_sat = sat_dict[forward]
            back_sat = sat_dict[back]
            G.add_edge(sat, forward_sat, weight=get_distance_between_two_sat(sat, forward_sat, t))
            G.add_edge(sat, back_sat, weight=get_distance_between_two_sat(sat, back_sat, t))

        left, right = sat.get_extra_sats(t)
        if left != '0_0' and right != '0_0':
            data["link"].append([sat.name, left])
            data["link"].append([sat.name, right])
            left_sat = sat_dict[left]
            right_sat = sat_dict[right]
            G.add_edge(sat, left_sat, weight=get_distance_between_two_sat(sat, left_sat, t))
            G.add_edge(sat, right_sat, weight=get_distance_between_two_sat(sat, right_sat, t))

    print("开始计算卫星-地面站链路~~~~~~~~~~~~~~~~~~~~~~~~")
    for gs in gs_list:
        linked_sat_dict = gs.get_link_sat(t)
        print(linked_sat_dict, type(linked_sat_dict))
        if linked_sat_dict is None:
            continue
        data['link'].append([gs.name, linked_sat_dict[1]])
        print([gs.name, linked_sat_dict[1]])
        linked_sat = sat_dict[linked_sat_dict[1]]
        distance = linked_sat_dict[0]
        G.add_edge(gs, linked_sat, weight=distance)

    # link去重
    res = list(set(tuple(sorted(sub)) for sub in data["link"]))
    data['link'] = res

    print(f"开始计算{gs_list[0].name} - {gs_list[1].name}的路径~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    path = []
    count = 0
    if nx.has_path(G, source=gs_list[0], target=gs_list[1]):
        p1 = nx.dijkstra_path(G, source=gs_list[0], target=gs_list[1])
        for node in p1:
            if type(node) == Satellite:
                count += 1
            path.append(node.name)
        data["path"] = path
        data["satNum"] = count
        p2 = nx.dijkstra_path_length(G, source=gs_list[0], target=gs_list[1])
        data["dis"] = p2

    fileName = '../../test/data.json'
    print(f"将计算结果写入文件: {fileName}~~~~~~~~~~~~~~~~~~~~~")
    with open(fileName, 'w') as f:
        json.dump(data, f)

import numpy as np
from datetime import datetime, timedelta
from sat.tool.time_tools import get_ts_from_time
def test_czml():
    sat_dict = auto_get_sat_dict('../test.yaml')

    initialTime = '2023-03-01T00:00:00Z'
    endTime = '2023-03-02T00:00:00Z'

    start_time = datetime.strptime(initialTime, '%Y-%m-%dT%H:%M:%SZ')
    end_time = datetime.strptime(endTime, '%Y-%m-%dT%H:%M:%SZ')

    minsInDuration = (end_time-start_time).total_seconds() / 60 ## 仿真持续时长, 以min为单位

    minsPerInterval = 1440 / 15.06  ## 卫星绕行一圈所用时长

    tempCZML = [] ## 储存CZMl
    tempCZML.append({
        "id": "document",
        "name": "CZML Point - Time Dynamic",
        "version": "1.0",
        "clock": {
            "interval": f'{initialTime}/{endTime}',
            "multiplier": 1,
            "range": "LOOP_STOP",
            "step": "SYSTEM_CLOCK"
        }
    },
    )

    # 计算path中的属性
    leadIntervalArray = []
    trailIntervalArray = []

    interval_time = end_time
    for i in np.arange(minsInDuration-minsPerInterval,  -minsPerInterval, -minsPerInterval):
        delta_time = timedelta(minutes=i)
        if i < 0:
            currentOrbitalInterval = {
                "interval": f'{start_time.isoformat()}Z/{interval_time.isoformat()}Z',
                "epoch": f'{start_time.isoformat()}Z',
                "number": [
                    0, minsPerInterval * 60,
                    minsPerInterval * 60, 0
                ]
            }
            currTrail = {
                "interval": f'{start_time.isoformat()}Z/{interval_time.isoformat()}Z',
                "epoch": f'{start_time.isoformat()}Z',
                "number": [
                    0, 0,
                    minsPerInterval * 60, minsPerInterval * 60
                ]
            }
            leadIntervalArray.append(currentOrbitalInterval)
            trailIntervalArray.append(currTrail)
        else:
            currentOrbitalInterval = {
                "interval": f'{(start_time + delta_time).isoformat()}Z/{interval_time.isoformat()}Z',
                "epoch": f'{(start_time + delta_time).isoformat()}Z',
                "number": [
                    0, minsPerInterval * 60,
                       minsPerInterval * 60, 0
                ]
            }
            currTrail = {
                "interval": f'{(start_time + delta_time).isoformat()}Z/{interval_time.isoformat()}Z',
                "epoch": f'{(start_time + delta_time).isoformat()}Z',
                "number": [
                    0, 0,
                    minsPerInterval * 60, minsPerInterval * 60
                ]
            }
            leadIntervalArray.append(currentOrbitalInterval)
            trailIntervalArray.append(currTrail)

            interval_time = start_time + delta_time

    ## 遍历所有卫星, 并生成packet
    for key, sat in sat_dict.items():
        show_path = False
        show_label = False
        if key.split('_')[1] == '1':
            show_path = True
            show_label = True
        positions = []
        scale = 300 ## 计算间隔, 单位s
        ## 计算惯性系(ECI)系中的坐标
        for i in np.arange(0, minsInDuration * 60 + scale, scale):
            # position = sat.get_blh(start_ts + i * 1.150470474e-5)
            # positions.append(i)
            # positions.append(position[1].degrees)
            # positions.append(position[0].degrees)
            # positions.append(position[2].m)

            t = get_ts_from_time(start_time + timedelta(seconds=i)) ## 提升精度
            position = sat.get_xyz_eci(t) ## 1s = 1.1574074074e-5天
            positions.append(i)
            positions.append(position[0])
            positions.append(position[1])
            positions.append(position[2])

        initialCZMLProps = {
            "id": f'{sat.name}',
            "name": f'{sat.name}',
            "availability": f'{initialTime}/{endTime}',
            "label": {
                "fillColor": {
                    "rgba": [
                        255, 0, 255, 255
                    ]
                },
                "font": "11pt Lucida Console",
                "horizontalOrigin": "LEFT",
                "outlineColor": {
                    "rgba": [
                        0, 0, 0, 255
                    ]
                },
                "outlineWidth": 2,
                "pixelOffset": {
                    "cartesian2": [
                        12, 0
                    ]
                },
                "show": show_label,
                "style": "FILL_AND_OUTLINE",
                "text": f'{sat.name}',
                "verticalOrigin": "CENTER"
            },
            "path": {
                "show": [
                    {
                        "interval": f'{initialTime}/{endTime}',
                        "boolean": show_path
                    }
                ],
                "width": 1,
                "material": {
                    "solidColor": {
                        "color": {
                            "rgba": [
                                math.floor(255 * random.random()), math.floor(255 * random.random()),
                                math.floor(255 * random.random()), 255
                            ]
                        }
                    }
                },
                "resolution": 120,
                "leadTime": leadIntervalArray,
                "trailTime": trailIntervalArray
            },
            "point": {
                "color": {
                    "rgba": [255,0,0,255]
                },
                "pixelSize": 5,
                "show": True
            },
            "position": {
                "interpolationAlgorithm": "LAGRANGE",
                "interpolationDegree": 5,
                # 参考坐标系，地惯坐标系
                "referenceFrame": "INERTIAL",
                "epoch": f'{initialTime}',
                "cartesian": positions
            }
        }
        tempCZML.append(initialCZMLProps)

    fileName = 'sat.czml'
    with open(fileName, 'w') as f:
        json.dump(tempCZML, f)

def test_gs_to_sat():
    sat_dict = auto_get_sat_dict()
    gs_list = auto_get_gs_list(sat_dict)

    gs = gs_list[0:2]

    initialTime = '2023-03-01T00:00:00Z'
    endTime = '2023-03-02T00:00:00Z'

    start_time = datetime.strptime(initialTime, '%Y-%m-%dT%H:%M:%SZ')
    end_time = datetime.strptime(endTime, '%Y-%m-%dT%H:%M:%SZ')
    start_ts = get_ts_from_time(start_time)
    end_ts = get_ts_from_time(end_time)

    minsInDuration = (end_time - start_time).total_seconds() / 60  ## 仿真持续时长, 以min为单位

    minsPerInterval = 1440 / 15.06  ## 卫星绕行一圈所用时长

    scale = 1
    result = []
    for i in np.arange(0, minsInDuration * 60 + scale, scale):
        t = start_ts + i * 1.1574074074e-5
        G = create_topo(sat_dict, gs, t)
        temp_result = calc_shortest_path(G, gs[0], gs[1], t)
        result.append(temp_result)

def create_topo(sat_dict, gs_list, t:skyfield.api.Time) -> networkx.Graph:
    print(f'{datetime.now().isoformat()}  开始生成图: {gs_list[0]} to {gs_list[1]}, {t.utc_iso()}')
    G = nx.Graph()
    G.add_nodes_from(sat_dict.values())
    G.add_nodes_from(gs_list)

    for sat in sat_dict.values():
        forward, back = sat.get_intra_sats(t)
        if forward is not None and back is not None:
            forward_sat = sat_dict[forward]
            back_sat = sat_dict[back]
            G.add_edge(sat, forward_sat, weight=get_distance_between_two_sat(sat, forward_sat, t))
            G.add_edge(sat, back_sat, weight=get_distance_between_two_sat(sat, back_sat, t))

        left, right = sat.get_extra_sats(t)
        if left != '0_0' and right != '0_0':
            left_sat = sat_dict[left]
            right_sat = sat_dict[right]
            G.add_edge(sat, left_sat, weight=get_distance_between_two_sat(sat, left_sat, t))
            G.add_edge(sat, right_sat, weight=get_distance_between_two_sat(sat, right_sat, t))

    for gs in gs_list:
        linked_sat_dict = gs.get_link_sat(t)
        if linked_sat_dict is None:
            continue
        linked_sat = sat_dict[linked_sat_dict[1]]
        distance = linked_sat_dict[0]
        G.add_edge(gs, linked_sat, weight=distance)

    return G

def calc_shortest_path(graph : networkx.Graph, source, dest, t:skyfield.api.Time) -> dict:
    print(f'{datetime.now().isoformat()}  正在计算最短路径: {source.name} to {dest.name}, {t.utc_iso()}')
    result = {
        "time": f'{t.utc_iso()}',
        "path": [],
        "sat num": 0,
        "dis": math.inf
    }

    count = 0
    path = []
    if nx.has_path(graph, source=source, dest=dest):
        p1 = nx.dijkstra_path(graph, source=source, target=dest)
        for node in p1:
            if type(node) == Satellite:
                count += 1
            path.append(node.name)
        p2 = nx.dijkstra_path_length(graph, source=source, dest=dest)

        result['path'] = path
        result['sat num'] = count
        result['dis'] = p2

    return result

def test_calc_json():
    # TODO: 时间有可能是多段的, 不能简单的排序
    with open('../data/2023-03-31_11-13-37/beijing China to London UK.json') as f:
        data = json.load(f)

    result = []

    # 对结果进行排序并分组
    groups = itertools.groupby(sorted(data, key=lambda x: x['path']), key=lambda x: x['path'])
    for key, group in groups:
        temp = {
            "path": [],
            "interval": ''
        }
        group_list = list(group)
        temp['path'] = key

        start = group_list[0]['time']

        # 修正时间, 使结束时间无下一个开始时间衔接
        end = group_list[-1]['time']
        end_iso = end.replace('Z', '')
        end_time = datetime.fromisoformat(end_iso)
        conf = get_yaml('../conf.yaml')
        timescale = conf['timescale']
        delta = timedelta(milliseconds=timescale)
        end = (end_time + delta).isoformat()

        temp['interval'] = f'{start}/{end}Z'

        result.append(temp)

    dir_path = '../data/test/'
    if os.path.exists(dir_path):
        os.makedirs(dir_path)
    filename = 'path.json'

    with open(dir_path+filename, 'w') as f:
        json.dump(result, f)

def create_line_czml():
    with open('../data/test/path.json') as f:
        data = json.load(f)
    result = []

    for d in data:
        path = d['path']




if __name__ == '__main__':
    # test_yaml()
    # test_networkx()
    # test_sat()
    # test_0()
    # test_sort()
    # test_json()
    test_czml()
    # test_calc_json()
