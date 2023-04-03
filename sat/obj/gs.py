from skyfield.api import wgs84

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