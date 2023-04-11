import json
import os
import arrow
import numpy as np
import math, random
from datetime import timedelta
from collections import defaultdict

from sat.tool.file_tools import get_yaml
from sat.tool.sat_tools import auto_get_sat_dict
from sat.tool.gs_tools import auto_get_gs_list
from sat.tool.time_tools import get_ts_from_time

def init_czml(start_iso, end_iso) -> dict:
    """
    初始化czml中必要的部分
    """
    print(f'{arrow.now().isoformat()}  初始化czml文件')
    doc = {
        "id": "document",
        "name": "CZML Point - Time Dynamic",
        "version": "1.0",
        "clock": {
            "interval": f'{start_iso}/{end_iso}',
            "multiplier": 1,
            "range": "LOOP_STOP",
            "step": "SYSTEM_CLOCK"
        }
    }
    return doc

def sat_czml(czml: list, sat_dict: dict, start_iso: str, end_iso: str) -> None:
    """
    将卫星添加到czml中
    """
    start_arrow = arrow.get(start_iso)
    end_arrow = arrow.get(end_iso)

    minsInDuration = (end_arrow-start_arrow).total_seconds() / 60 ## 仿真持续时长, 以min为单位

    minsPerInterval = 1440 / 15.06  ## 卫星绕行一圈所用时长

    # 计算path中的属性
    leadIntervalArray = []
    trailIntervalArray = []

    interval_time = end_arrow
    for i in np.arange(minsInDuration-minsPerInterval,  -minsPerInterval, -minsPerInterval):
        delta_time = timedelta(minutes=i)
        if i < 0:
            currentOrbitalInterval = {
                "interval": f'{start_arrow.isoformat()}/{interval_time.isoformat()}',
                "epoch": f'{start_arrow.isoformat()}',
                "number": [
                    0, minsPerInterval * 60,
                    minsPerInterval * 60, 0
                ]
            }
            currTrail = {
                "interval": f'{start_arrow.isoformat()}/{interval_time.isoformat()}',
                "epoch": f'{start_arrow.isoformat()}',
                "number": [
                    0, 0,
                    minsPerInterval * 60, minsPerInterval * 60
                ]
            }
            leadIntervalArray.append(currentOrbitalInterval)
            trailIntervalArray.append(currTrail)
        else:
            currentOrbitalInterval = {
                "interval": f'{(start_arrow + delta_time).isoformat()}/{interval_time.isoformat()}',
                "epoch": f'{(start_arrow + delta_time).isoformat()}',
                "number": [
                    0, minsPerInterval * 60,
                       minsPerInterval * 60, 0
                ]
            }
            currTrail = {
                "interval": f'{(start_arrow + delta_time).isoformat()}/{interval_time.isoformat()}',
                "epoch": f'{(start_arrow + delta_time).isoformat()}',
                "number": [
                    0, 0,
                    minsPerInterval * 60, minsPerInterval * 60
                ]
            }
            leadIntervalArray.append(currentOrbitalInterval)
            trailIntervalArray.append(currTrail)

            interval_time = start_arrow + delta_time

    ## 遍历所有卫星, 并生成packet
    for key, sat in sat_dict.items():
        print(f'{arrow.now().isoformat()}  正在计算{key}的czml文件')
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

            t = get_ts_from_time(start_arrow + timedelta(seconds=i)) ## 提升精度
            position = sat.get_xyz_eci(t) ## 1s = 1.1574074074e-5天
            positions.append(i)
            positions.append(position[0])
            positions.append(position[1])
            positions.append(position[2])

        initialCZMLProps = {
            "id": f'{sat.name}',
            "name": f'{sat.name}',
            "availability": f'{start_iso}/{end_iso}',
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
                        "interval": f'{start_iso}/{end_iso}',
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
                "epoch": f'{start_iso}',
                "cartesian": positions
            }
        }
        czml.append(initialCZMLProps)

def gs_czml(czml: list, gs_list: list):
    """
    将地面站添加到czml中
    """
    print(f'{arrow.now().isoformat()}  正在计算地面站的czml文件')
    is_label_show = True
    for gs in gs_list:
        name = gs.name
        x,y,z = gs.get_xyz()
        czml_temp = {
            "id": f"{name}",
            "name": f"{name}",
            "label": {
                "fillColor": {
                    "rgba": [
                        0,
                        255,
                        255,
                        255
                    ]
                },
                "font": "11pt Lucida Console",
                "horizontalOrigin": "LEFT",
                "outlineColor": {
                    "rgba": [
                        0,
                        0,
                        0,
                        255
                    ]
                },
                "outlineWidth": 2,
                "pixelOffset": {
                    "cartesian2": [
                        12,
                        0
                    ]
                },
                "show": is_label_show,
                "style": "FILL_AND_OUTLINE",
                "text": f"{name}",
                "verticalOrigin": "CENTER"
            },
            "position": {
                "cartesian": [
                    x,
                    y,
                    z
                ]
            }
        }
        czml.append(czml_temp)

def line_czml(czml: list, dir_path, filename):
    """
    将链路添加到czml中
    """
    print(f'{arrow.now().isoformat()}  正在计算路径的czml文件')

    res = _calc_line(dir_path, filename)

    for line in res:
        czml_temp = {
            "id": f"{line['path'][0]}-to-{line['path'][1]}",
            "name": f"{line['path'][0]}-to-{line['path'][1]}",
            "availability": [],
            "polyline": {
                "show": [],
                "width": 1,
                "material": {
                    "solidColor": {
                        "color": {
                            "rgba": [
                                0,
                                255,
                                255,
                                255
                            ]
                        }
                    }
                },
                "arcType": "NONE",
                "positions": {
                    "references": [
                        f"{line['path'][0]}#position",
                        f"{line['path'][1]}#position"
                    ]
                }
            }
        }
        intervals = line['interval']

        # 开头不可见时间
        temp = {"interval": f"0000-01-01T00:00:00Z/{intervals[0][0]}", "boolean": False}
        czml_temp['polyline']['show'].append(temp)
        # 结尾不可见时间
        temp = {"interval": f"{intervals[-1][1]}/9999-12-31T24:00:00Z", "boolean": False}
        czml_temp['polyline']['show'].append(temp)

        i = 0
        while i < len(intervals):
            # 添加availability数组
            czml_temp['availability'].append(f'{intervals[i][0]}/{intervals[i][1]}')

            # 添加可见时间段
            temp = {"interval": f"{intervals[i][0]}/{intervals[i][1]}", "boolean": True}
            czml_temp['polyline']['show'].append(temp)
            # 添加不可见时间段
            if i+1 < len(intervals):
                temp = {"interval": f"{intervals[i][1]}/{intervals[i+1][0]}", "boolean": False}
                czml_temp['polyline']['show'].append(temp)
            i += 1

        czml.append(czml_temp)


def _calc_line(dir_path, filename):
    """
    将路径按照时间排序, 并合并
    """
    with open(dir_path+filename) as f:
        data = json.load(f)

    res = defaultdict(list)
    # 按照路径划分, 并添加对应的时间
    for item in data:
        path_list = item['path']
        time = item['time']
        i = 1
        while i < len(path_list)-1:
            res[tuple(path_list[i-1:i+1])].append(time)
            i += 1
    # 对时间数组进行排序
    for value in res.values():
        value.sort()

    result = []
    delta_def = timedelta(seconds=1)
    # 合并路径中连续的时间
    for key, value in res.items():
        start = 0
        end = 1
        temp = {
            "path": [],
            "interval": []
        }
        temp['path'].extend(key)
        while end < len(value):
            delta = arrow.get(value[end]) - arrow.get(value[end-1])
            while end < len(value) and delta == delta_def:
                end += 1
            # 修正时间, 使时间连续, 前闭后开
            end_arrow = arrow.get(value[end-1])
            end_arrow = end_arrow + delta_def
            # temp['interval'].append(f'{value[start]}/{end_arrow.isoformat()}')
            temp['interval'].append(tuple([value[start], end_arrow.isoformat()]))
            start = end
        result.append(temp) # 将每一个线条加入数组

    return result

def all_czml(dir_path, filename, conf_path ='../conf.yaml'):
    """
    生成czml文件

    :param dir_path: str, 路由计算结果所在的文件路径
    :param filename: str, 路由计算结果的文件名
    :param conf_path: str, 配置文件所在路径
    """
    conf = get_yaml(conf_path)
    start_iso = conf['start']
    end_iso = conf['end']

    sat_dict = auto_get_sat_dict(conf_path)
    gs_list = auto_get_gs_list(sat_dict, conf_path)

    czml = [init_czml(start_iso, end_iso)]
    sat_czml(czml, sat_dict, start_iso, end_iso)
    gs_czml(czml, gs_list)
    # line_czml(czml, dir_path, filename)

    return czml

def save_czml(czml: list, dir_path, filename = 'sat.czml') -> None:
    """
    将czml保存到文件中, filename = sat.czml
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    print(f'{arrow.now().isoformat()}  正在保存场景czml文件')
    with open(dir_path+filename, 'w') as f:
        json.dump(czml, f)

def auto_czml(save_file_dir_path, calc_dir_path, calc_filename, save_filename ='sat.czml', conf_path ='../conf.yaml'):
    """
    自动生成czml文件并保存到磁盘.
    :param save_file_dir_path: str, 生成的czml文件的保存路径
    :param save_filename: str, 生成的czml文件的名称
    :param calc_dir_path: str, 路由计算结果所在的文件路径
    :param calc_filename: str, 路由计算结果的文件名
    :param conf_path: str, 配置文件所在路径
    """
    czml = all_czml(calc_dir_path, calc_filename, conf_path)
    save_czml(czml, save_file_dir_path, filename=save_filename)

if __name__ == '__main__':
    # _calc_line('../data/2023-04-10_14-46-40/', 'beijing China to London UK.json')
    # czml = []
    # sat_dict = auto_get_sat_dict('../test.yaml')
    # gs_list = auto_get_gs_list(sat_dict, '../test.yaml')
    # line_czml(czml, '../data/2023-04-10_09-15-11/', 'beijing China to London UK.json')
    # save_czml(czml, '../data/2023-04-10_14-46-40/', 'line.czml')

    auto_czml('../data/2023-04-10_09-15-11/',
              '../data/2023-04-10_09-15-11/',
              'beijing China to London UK.json',
              save_filename ='sat.czml',
              conf_path ='../test.yaml')
