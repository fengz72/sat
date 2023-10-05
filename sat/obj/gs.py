from skyfield.api import wgs84
import numpy as np

class GroundStation:
    def __init__(self, name, lat, lon, height, degree, sat_dict):
        self.name = name
        self.gs = wgs84.latlon(lat, lon, height)
        self.degree = degree
        self.sat_dict = sat_dict

    def get_link_sat(self, t):
        """
        计算连接的卫星, 最短距离策略, 限制: 通信门限高于设定值; 无可连接卫星时返回None
        :param t: 时间: skyfield.timelib.Time
        :return: (distance: m, orbit_num: String): tuple
        """
        link_sat = {}
        for key, value in self.sat_dict.items():
            dif = value.sat - self.gs
            alt, az, distance = dif.at(t).altaz()

            # print(t.utc_strftime('%Y-%m-%d %H:%M:%S') + ' ' + self.name + ' degrees: ' + str(alt.degrees))
            if alt.degrees >= self.degree:
                link_sat[key] = distance.km * 1000
                # print(t.utc_strftime('%Y-%m-%d %H:%M:%S') + ' ' + self.name + ' sat: ' + key + ' degrees: ' + str(alt.degrees) + ' dis: ' + str(distance.km * 1000) + 'm')


        linked_sat = None
        if len(link_sat) != 0:
            linked_sat = min(zip(link_sat.values(), link_sat.keys()))
        return linked_sat
    def shortest_link_sat_random(self, t, error, right_sat):
        min_dis = 1e9
        name = ''
        gs_pos = self.gs.itrs_xyz.m
        for key, sat in self.sat_dict.items():
            sat_pos = sat.get_xyz_random(t, error)
            dis = np.linalg.norm(gs_pos - sat_pos)
            if dis < min_dis and self.orbit_delta(key, right_sat):
                min_dis = dis
                name = key
        return name

    def orbit_delta(self, key1, key2):
        orbit1 = int(key1.split('_')[0])
        orbit2 = int(key2.split('_')[0])

        lat = self.sat_dict['1_1'].num_orbits
        return abs(orbit1 - orbit2) <= lat / 2

    def shortest_link_sat(self, t):
        min_dis = 1e9
        name = ''
        gs_pos = self.gs.itrs_xyz.m
        for key, sat in self.sat_dict.items():
            sat_pos = sat.get_xyz_m(t)
            dis = np.linalg.norm(gs_pos - sat_pos)
            if dis < min_dis:
                min_dis = dis
                name = key
        return name

    def get_blh(self):
        """
        计算wgs84坐标系下的大地坐标, 角度单位: °, 高度单位: m
        :return: (lat, lon, height): Tuple
        """
        return self.gs.latitude.degrees, self.gs.longitude.degrees, self.gs.elevation.m

    def get_xyz(self):
        """
        计算itrs坐标系下的坐标, 单位: m
        :return: (x, y, n): ndarray
        """
        return self.gs.itrs_xyz.m