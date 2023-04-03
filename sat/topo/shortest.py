import json
import os
from datetime import datetime
import math

import skyfield.api
from skyfield.api import load
import networkx as nx

from sat.obj.sat import Satellite
from sat.tool.distance_tools import get_distance_between_two_sat
from sat.tool.gs_tools import auto_get_gs_list
from sat.tool.sat_tools import auto_get_sat_dict, save_tles_to_file
from sat.tool.time_tools import get_ts_from_std, get_ts_array_from_std
from sat.tool.file_tools import get_yaml
from sat.topo.topo import create_topo


def calc_one(sat_path, gs_path, t_str):
    sat_dict = auto_get_sat_dict(sat_path)
    gs_list = auto_get_gs_list(sat_dict, gs_path)

    t = get_ts_from_std(t_str)

    time_str = t.utc_strftime('%Y-%m-%dT%H:%M:%SZ')
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

    start = 0
    end = 2
    print(f"开始计算{gs_list[start].name} - {gs_list[end].name}的路径~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    path = []
    count = 0
    if nx.has_path(G, source=gs_list[start], target=gs_list[end]):
        p1 = nx.dijkstra_path(G, source=gs_list[start], target=gs_list[end])
        for node in p1:
            if type(node) == Satellite:
                count += 1
            path.append(node.name)
        data["path"] = path
        data["satNum"] = count
        p2 = nx.dijkstra_path_length(G, source=gs_list[start], target=gs_list[end])
        data["dis"] = p2

    fileName = f'../test/{gs_list[start].name} to {gs_list[end].name}/{str(t.utc_strftime("%Y-%m-%d %H-%M-%S"))}.json'
    print(f"将计算结果写入文件: {fileName}~~~~~~~~~~~~~~~~~~~~~")
    with open(fileName, 'w') as f:
        json.dump(data, f)

# 传播速度
c = 291020.9 * 1000
# 排队时延 0.5ms
node_delay = 0.5

def calc_txt(sat_path, gs_path, start_str, end_str, timescale, dir_path):
    sat_dict = auto_get_sat_dict(sat_path)
    gs_list = auto_get_gs_list(sat_dict, gs_path)

    ts = load.timescale()
    t1= ts.utc(2023, 3, 1, 0, 0, 0)
    t2= ts.utc(2023, 3, 1, 0, 4, 59)
    t_array = ts.linspace(t1, t2, 300)

    start = 0
    end = 2
    dir_path = f'../test/{gs_list[start].name} to {gs_list[end].name}'
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    for tt in t_array:

        G = nx.Graph()
        G.add_nodes_from(sat_dict.values())
        G.add_nodes_from(gs_list)

        time_str = tt.utc_strftime('%Y-%m-%dT%H:%M:%SZ')
        data = {
            "time": time_str,
            # "sat": [{sat.name: [sat.get_blh(t)[0].degrees, sat.get_blh(t)[1].degrees, sat.get_blh(t)[2].m]} for sat in sat_dict.values()],
            "sat": [{'name': sat.name, 'pos': list(sat.get_xyz(tt) * 1000)} for sat in sat_dict.values()],
            "gs": [{'name': gs.name, 'pos': list(gs.get_xyz())} for gs in gs_list],
            "link": [],
            "path": [],
            "dis": 0,
            "satNum": 0
        }

        print("开始计算卫星间链路~~~~~~~~~~~~~~~~~~~~~~~~")
        for sat in sat_dict.values():
            forward, back = sat.get_intra_sats(tt)
            if forward is not None and back is not None:
                data["link"].append([sat.name, forward])
                data["link"].append([sat.name, back])
                forward_sat = sat_dict[forward]
                back_sat = sat_dict[back]
                G.add_edge(sat, forward_sat, weight = get_distance_between_two_sat(sat, forward_sat, tt))
                G.add_edge(sat, back_sat, weight = get_distance_between_two_sat(sat, back_sat, tt))

            left, right = sat.get_extra_sats(tt)
            if left != '0_0' and right != '0_0':
                data["link"].append([sat.name, left])
                data["link"].append([sat.name, right])
                left_sat = sat_dict[left]
                right_sat = sat_dict[right]
                G.add_edge(sat, left_sat, weight = get_distance_between_two_sat(sat, left_sat, tt))
                G.add_edge(sat, right_sat, weight = get_distance_between_two_sat(sat, right_sat, tt))

        print("开始计算卫星-地面站链路~~~~~~~~~~~~~~~~~~~~~~~~")
        for gs in gs_list:
            linked_sat_dict = gs.get_link_sat(tt)
            if linked_sat_dict is None:
                continue
            data['link'].append([gs.name, linked_sat_dict[1]])
            linked_sat = sat_dict[linked_sat_dict[1]]
            distance = linked_sat_dict[0]
            G.add_edge(gs, linked_sat, weight = distance)

        # link去重
        res = list(set(tuple(sorted(sub)) for sub in data["link"]))
        data['link'] = res

        filename = 'data.txt'
        with open(dir_path + '/' + filename, 'a', encoding='utf-8') as f:
            f.write('time: ' + str(tt.utc_strftime('%Y-%m-%d %H:%M:%S')) + "\n")
            f.write(gs_list[start].name + ' to ' + gs_list[end].name + ': \n')

            if nx.has_path(G, source=gs_list[start], target=gs_list[end]):
                path = []
                count = 0
                p2 = 0
                p1 = nx.dijkstra_path(G, source=gs_list[start], target=gs_list[end])
                for node in p1:
                    if type(node) == Satellite:
                        count += 1
                    path.append(node.name)
                data["path"] = path
                data["satNum"] = count
                p2 = nx.dijkstra_path_length(G, source=gs_list[start], target=gs_list[end])
                data["dis"] = p2
                delay = p2 / c * 1000 + count * node_delay

                path_str = ', '.join(path)
                f.write(path_str + '\n')
                f.write('sat num: ' + str(count) + '\n')
                f.write('dis: ' + str(p2 /1000) + ' km\n')
                f.write('delay: ' + str(delay) + ' ms\n\n')
            else:
                f.write(' ' + '\n')
                f.write('sat num: 0' + '\n')
                f.write('dis: inf' + ' km\n')
                f.write('delay: inf' + ' ms\n\n')

            # if tt in [ts.utc(2023, 3, 1, 0, 0, 57), ts.utc(2023, 3, 1, 0, 0, 58)]:
            #     fileName = f'../test/{gs_list[start].name} to {gs_list[end].name}/{str(tt.utc_strftime("%Y-%m-%d %H-%M-%S"))}.json'
            #     print(f"将计算结果写入文件: {fileName}~~~~~~~~~~~~~~~~~~~~~")
            #     with open(fileName, 'w') as f:
            #         json.dump(data, f)

def calc_shortest_path(graph : nx.Graph, source, dest, t:skyfield.api.Time) -> dict:
    print(f'{datetime.now().isoformat()}  正在计算最短路径: {source.name} to {dest.name}, {t.utc_iso()}')
    result = {
        "time": f'{t.utc_iso()}',
        "path": [],
        "sat num": 0,
        "dis": math.inf
    }

    count = 0
    path = []
    if nx.has_path(graph, source=source, target=dest):
        p1 = nx.dijkstra_path(graph, source=source, target=dest)
        for node in p1:
            if type(node) == Satellite:
                count += 1
            path.append(node.name)
        p2 = nx.dijkstra_path_length(graph, source=source, target=dest)

        result['path'] = path
        result['sat num'] = count
        result['dis'] = p2

    return result

def calc_all(conf_path = '../conf.yaml'):
    # 得到文件保存路径
    time_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    dir_path = f'../data/{time_str}/'
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    # 根据配置文件, 生成卫星和地面站
    sat_dict = auto_get_sat_dict(conf_path)
    gs_list = auto_get_gs_list(sat_dict, conf_path)

    conf = get_yaml(conf_path)
    start_std = conf['start']
    end_std = conf['end']
    timescale = conf['timescale']
    name = conf['name']
    tle_save = conf['tle_save']

    # 保存tle文件
    if tle_save:
        save_tles_to_file(sat_dict, name, dir_path)

    ts_array = get_ts_array_from_std(start_std, end_std, timescale) # 根据时间间隔得到时间数组
    # 计算第一个地面站到其他地面站的最短路径
    for gs in gs_list[1:]:
        filename = f'{gs_list[0].name} to {gs.name}.json'
        result = []
        for ts in ts_array:
            g = create_topo(sat_dict, gs_list, ts)
            temp = calc_shortest_path(g, gs_list[0], gs, ts)
            result.append(temp)
        #保存数据到文件
        print(f'{datetime.now().isoformat()}  将计算结果写入文件: {gs_list[0].name} to {gs.name}')
        with open(dir_path+filename, 'w') as f:
            json.dump(result, f)


if __name__ == "__main__":
    calc_all()

