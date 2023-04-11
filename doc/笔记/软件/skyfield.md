# skyfield

## 1 基础
设置时间
```python
from skyfield.api import load
ts = load.timescale()
t = ts.now()
# ts.utc(2022, 10, 24, 16, 46, 10)
```

导入tle
```python
from skyfield.api import load, wgs84
stations_url = 'http://celestrak.com/NORAD/elements/stations.txt'
satellites = load.tle_file(stations_url)
```

遍历卫星
```python
by_name = {sat.name: sat for sat in satellites}
satellite = by_name['ISS (ZARYA)']
print(satellite)
# ISS (ZARYA) catalog #25544 epoch 2022-10-24 04:54:22 UTC

by_num = {sat.model.satnum: sat for sat in satellites}
satellite = by_num[25544]
print(satellite)
# ISS (ZARYA) catalog #25544 epoch 2022-10-24 04:54:22 UTC
```

satellite.epoch: tle的生成时间
```python
satellite.epoch
# <Time tt=2459876.705227361>
satellite.epoch.utc_jpl()
# 'A.D. 2022-Oct-24 04:54:22.4600 UTC'
```

得到GCRS坐标基下的(x, y, z)位置
```python
geocentric = satellite.at(t)
geocentric.position.km
# array([-539.3914417 , 5265.70421807, 4249.4420094 ])
geocentric.position.km[0]
# -539.3914416959032
```

得到经纬度, 高度
```python
lat, lon = wgs84.latlon_of(geocentric)
# lat
# <Angle 38deg 55' 21.7">
# lon
# <Angle -55deg 51' 22.7">
wgs84.height_of(geocentric).km
# 418.218937367963
wgs84.geographic_position_of(geocentric)
# <GeographicPosition WGS84 latitude +38.9227 N longitude -55.8563 E elevation 418218.9 m>
```

得到两个卫星之间的距离
```python
sat01 = by_name['AEROCUBE 12A']
sat02 = by_name['AEROCUBE 12B']
difference = sat02 - sat01
topocentric = difference.at(t)
# ICRF
dist = topocentric.position.km
# [ -929.07660342 -7643.3995251  -2564.00224794]
math.sqrt(dist[0]**2+dist[1]**2+dist[2]**2)
```

![](https://img-1258201770.cos.ap-beijing.myqcloud.com/imgs/ca71517bee80745017b1ce7cda705960.png)

![](https://img-1258201770.cos.ap-beijing.myqcloud.com/imgs/b7e2f518f128cf76e410bee3c359419a.png)

[skyfield](https://rhodesmill.org/skyfield/earth-satellites.html)
[sgp4](https://pypi.org/project/sgp4/)

## 2 temp
skyfield卫星获得坐标默认为ICRS(GCRS), 笛卡尔坐标(x, y, z)
```python
# Geocentric ICRS position and velocity
geocentric = sat.at(t)
# [-3918.87650458 -1887.64838745  5209.08801512]
geocentric.position.km
```

可以使用wg84获得地理坐标
```python
#Latitude: 50deg 14' 37.4"
#Longitude: -86deg 23' 23.3"
lat, lon = wgs84.latlon_of(geocentric)
```

### 2.1 altitude, azimuth, distance
高度角, 方位和距离
高度角小于0意味着在地平线以下
```python
difference = satellite - bluffton
topocentric = difference.at(t)
topocentric.position.km
alt, az, distance = topocentric.altaz()
alt.degrees
```

速率
```python
t = ts.utc(2014, 1, 23, 11, range(17, 23))
pos = (satellite - bluffton).at(t)
_, _, the_range, _, _, range_rate = pos.frame_latlon_and_rates(bluffton)

from numpy import array2string
print(array2string(the_range.km, precision=1), 'km')
print(array2string(range_rate.km_per_s, precision=2), 'km/s')

[1434.2 1190.5 1064.3 1097.3 1277.4 1553.6] km
[-4.74 -3.24 -0.84  1.9   3.95  5.14] km/s
```