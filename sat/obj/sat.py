from skyfield.framelib import itrs
from skyfield.api import wgs84
import numpy as np

class Satellite(object):
    def __init__(self, sat_name, satrec, skyfield_sat, num_orbits, num_sats_per_orbits, f):
        self.name = sat_name
        self.sat = skyfield_sat
        self.satrec = satrec
        self.num = skyfield_sat.model.satnum
        self.orbit = int(sat_name.split('_')[0])
        self.num_on_orbit = int(sat_name.split('_')[1])
        self.num_orbits = num_orbits
        self.num_sats_per_orbits = num_sats_per_orbits
        self.f = f

    def get_xyz(self, t):
        """
        计算t时刻itrs坐标系下的坐标, 单位: km
        :param t: 时间: skyfield.timelib.Time
        :return: (x, y, n): ndarray
        """
        position = self.sat.at(t)
        return position.frame_xyz(itrs).km

    def get_xyz_m(self, t):
        """
        计算t时刻itrs坐标系下的坐标, 单位: m
        :param t: 时间: skyfield.timelib.Time
        :return: (x, y, n): ndarray
        """
        position = self.sat.at(t)
        return position.frame_xyz(itrs).m

    def get_xyz_random(self, t, error):
        error = error / 100.0
        position = self.sat.at(t)
        loc = position.frame_xyz(itrs).m
        for i in range(0, 3):
            delta = np.random.uniform(-error, error)
            loc[i] = loc[i] * (1 + delta)

        return loc

    def get_xyz_eci(self, t):
        """
        计算惯性系下的位置
        """
        position = self.sat.at(t)
        return position.position.m

    def get_blh(self, t):
        """
        计算t时刻wgs84坐标系下的大地坐标
        :param t: 时间: skyfield.timelib.Time
        :return: (lat: Angle, lon: Angle, height: Distance): tuple
        """
        position = self.sat.at(t)
        lat, lon = wgs84.latlon_of(position)
        height = wgs84.height_of(position)
        return lat, lon, height

    def get_intra_sats(self, t):
        """
        计算轨内链路连接的卫星, 返回卫星的名称: '1_1', '1_3'
        :param t:
        :return: (forward, back): Tuple
        """
        if self.num_on_orbit - 1 == 0:
            forward_num = self.num_sats_per_orbits
        else:
            forward_num = (self.num_on_orbit - 1) % self.num_sats_per_orbits

        back_num = self.num_on_orbit % self.num_sats_per_orbits + 1
        return str(self.orbit) + '_' + str(forward_num), str(self.orbit) + '_'+ str(back_num)

    def get_extra_sats(self, t):
        """
        计算轨间链路连接的卫星, 返回卫星的名称: '1_1'
        :param t:
        :return: 不存在返回'0_0', '0_0'
        """
        if self.is_sat_close_extra_isl(t):
            return '0_0', '0_0'

        if self.orbit - 1 == 0:
            forward_orbit = self.num_orbits
        else:
            forward_orbit = (self.orbit - 1) % self.num_orbits
        back_orbit = self.orbit % self.num_orbits + 1

        return str(forward_orbit) + '_' + str(self.num_on_orbit), str(back_orbit) + '_' + str(self.num_on_orbit)

    def is_sat_close_extra_isl(self, t):
        """
        计算卫星关闭星间链路，取倾斜角度的90%为标准
        :param t:
        :return:
        """
        lat, lon, height = self.get_blh(t)
        return lat.radians > self.sat.model.inclo * 0.9



