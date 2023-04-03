import math
import os.path
import time
from datetime import datetime

import yaml
from sgp4.api import Satrec, WGS72
from sgp4 import exporter
from skyfield.api import EarthSatellite, load
from sat.obj.sat import Satellite
from sat.tool.file_tools import get_yaml
from sat.tool.time_tools import get_julian_from_time

# jd从公历的公元前4714年11月24日12:00计算
# epoch从1949 December 31 00:00 UT计算
time_diff = 2433281.5

def get_one_satrec_from_scratch(num_orbits,
                                num_sats_per_orbits,
                                num_orbit,
                                num_sat_on_orbit,
                                f,
                                jd,
                                fr,
                                ecco,
                                argpo,
                                inclo,
                                mean_motion_loop_per_day):
    """
    通过sgp4的WGS74库来初始化卫星

    :param num_orbits: 轨道数
    :param num_sats_per_orbits: 每轨卫星数
    :param num_orbit: 当前卫星的轨道, 从1开始
    :param num_sat_on_orbit: 当前卫星在轨道的编号, 从1开始
    :param f: 相位因子
    :param jd: julian day
    :param fr: jd的小数部分
    :param ecco: 偏心率
    :param argpo: 近地点辐角
    :param inclo: 轨道倾角
    :param mean_motion_loop_per_day: 卫星每天运动的天数
    """

    num_sat = (num_orbit - 1) * num_sats_per_orbits + num_sat_on_orbit

    mean_anomaly_degree = (360.0 / num_sats_per_orbits) * ((num_sat_on_orbit - 1) + f * (num_orbit - 1) / num_orbits) % 360
    # print(f"{mean_anomaly_degree} = (360.0 / {num_sats_per_orbits}) * (({num_sat_on_orbit} - 1) + {f} * ({num_orbit} - 1) / {num_orbits}) % 360")
    mean_motion_degree_minute = mean_motion_loop_per_day * 360 / (24 * 60)
    raan_degree = 360.0 / num_orbits * num_orbit

    satrec = Satrec()
    satrec.sgp4init(
        WGS72,  # gravity model
        'i',  # 'a' = old AFSPC mode, 'i' = improved mode
        num_sat,  # num_sat: Satellite number
        (jd + fr) - time_diff,  # epoch: days since 1949 December 31 00:00 UT
        0.0,  # bstar:   drag coefficient (kg/m2er)
        0.0,  # ndot: ballistic coefficient (revs/day)
        0.0,  # nndot:   second derivative of mean motion (revs/day^3)
        ecco,  # ecco: eccentricity, 偏心率
        math.radians(argpo),  # argpo: argument of perigee (radians), 近地点辐角
        math.radians(inclo),  # inclo: inclination (radians), 轨道与赤道的夹角
        math.radians(mean_anomaly_degree),  # mo: mean anomaly (radians), 平近点角
        math.radians(mean_motion_degree_minute),  # no_kozai: mean motion (radians/minute), 每分钟的弧度
        math.radians(raan_degree)  # nodeo: R.A. of ascending node (radians) RAAN: 升交点赤经
    )

    return satrec


def get_all_sat_from_scratch(num_orbits,
                             num_sats_per_orbits,
                             f,
                             jd,
                             fr,
                             ecco,
                             argpo,
                             inclo,
                             mean_motion_loop_per_day):
    """
    得到所有的卫星对象, 以字典返回. key: (num_orbit)_(num_sat_on_orbit)
    :param num_orbits:
    :param num_sats_per_orbits:
    :param f: 相位
    :param jd: julian日期
    :param fr: julian日期小数部分
    :param ecco: 离心率
    :param argpo: 近地点辐角
    :param inclo: 轨道倾角
    :param mean_motion_loop_per_day: 卫星每天运动圈数
    :return: sat_dict
    """
    sat_dict = {}
    ts = load.timescale()
    for i in range(1, num_orbits + 1):
        for j in range(1, num_sats_per_orbits + 1):
            sat_name = str(i) + '_' + str(j)
            # print(f"{sat_name}: ")
            satrec = get_one_satrec_from_scratch(num_orbits, num_sats_per_orbits, i, j, f,
                                                 jd, fr, ecco, argpo, inclo, mean_motion_loop_per_day)

            skyfield_sat = EarthSatellite.from_satrec(satrec, ts)
            sat = Satellite(sat_name, satrec, skyfield_sat, num_orbits, num_sats_per_orbits, f)
            sat_dict[sat_name] = sat
    return sat_dict

def auto_get_sat_dict(file_path='../conf.yaml'):
    """
    根据配置文件自动生成星座
    :param file_path:
    :return: {'1_1': Satellite}: dict
    """
    print(f"{datetime.now().isoformat()}    开始生成星座")
    result = get_yaml(file_path)

    jd, fr = get_julian_from_time(result['epoch'])
    sat_dict = get_all_sat_from_scratch(result['num_orbits'],
                                        result['num_sats_per_orbits'],
                                        result['f'],
                                        jd,
                                        fr,
                                        result['ecco'],
                                        result['argpo'],
                                        result['inclo'],
                                        result['mean_motion_loop_per_day'])
    return sat_dict

def save_tles_to_file(sat_dict, constellation_name, dir_path):
    """
    生成tle文件并保存.
    :param constellation_name: 星座名称
    :param sat_dict: 字典, <starlink_name, satrec>
    :param file_name: 保存的文件路径与名称
    :return:
    """
    file_name = constellation_name
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    file_path = dir_path + file_name + '.txt'

    print(f"{datetime.now().isoformat()}    正在保存星座TLE文件")

    file = ''
    for key, value in sat_dict.items():
        line1, line2 = exporter.export_tle(value.satrec)
        tle_line1, tle_line2 = _set_right_tle(line1, line2)
        file += constellation_name + '_' + key + '\n' + tle_line1 + '\n' + tle_line2 + '\n'

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(file)


def _set_right_tle(line1, line2):
    """
    手动矫正tle
    代码来自于https://github.com/snkas/hypatia/blob/master/satgenpy/satgen/tles/generate_tles_from_scratch.py
    :param line1:
    :param line2:
    :return:
    """
    tle_line1 = line1[:7] + "U 00000ABC " + line1[18:]
    tle_line1 = tle_line1[:68] + str(_calculate_tle_line_checksum(tle_line1[:68]))
    tle_line2 = line2
    # Check that the checksum is correct
    if len(tle_line1) != 69 or _calculate_tle_line_checksum(tle_line1[:68]) != int(tle_line1[68]):
        raise ValueError("TLE line 1 checksum failed")
    if len(tle_line2) != 69 or _calculate_tle_line_checksum(tle_line2[:68]) != int(tle_line2[68]):
        raise ValueError("TLE line 2 checksum failed")
    return tle_line1, tle_line2


def _calculate_tle_line_checksum(tle_line_without_checksum):
    if len(tle_line_without_checksum) != 68:
        raise ValueError("Must have exactly 68 characters")
    s = 0
    for i in range(len(tle_line_without_checksum)):
        if tle_line_without_checksum[i].isnumeric():
            s += int(tle_line_without_checksum[i])
        if tle_line_without_checksum[i] == "-":
            s += 1
    return s % 10