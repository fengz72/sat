import numpy as np

def get_distance_from_xyz(x, y, z):
    return np.linalg.norm([x, y, z])


def get_distance_from_array(distance_array):
    return np.linalg.norm(distance_array)


def get_distance_between_two_sat(v_sat, t_sat, t):
    """
    计算两个卫星之间的距离, 单位: m
    :param v_sat: Satellite
    :param t_sat: Satellite
    :param t:
    :return:
    """
    dif = v_sat.sat - t_sat.sat
    return get_distance_from_array(dif.at(t).position.km) * 1000