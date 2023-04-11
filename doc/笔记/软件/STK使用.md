# STK使用
## 1 入门
### 1.1 安装
百度网盘自己搜

### 1.2 连接python
- [csdn-STK二次开发Python的首次连接](https://blog.csdn.net/u011575168/article/details/86582961?utm_medium=distribute.pc_relevant.none-task-blog-baidujs-8)

## 2 卫星姿态
- 显示姿态球
  properties-3D-attitude Sphere - zoom to
- 显示速度向量
  properties-3D-Vector-Velocity Vector
### 2.1 VVLH坐标系及方位角、高度角
STK中，附着在卫星上的有许多坐标系，例如：VNC、LVLH、VVLH等。以及在定义某矢量方向时，需要使用方位角、高度角的概念。
VVLH坐标系和方位角(Az）、高度角(El)的示意见下图:
![](https://img-1258201770.cos.ap-beijing.myqcloud.com/imgs/d0dad42d53eba6052af333d0937873a7.png)

**VVLH**
VVLH坐标系全称为：Vehicle Velocity Local Horizontal coordinate system。
对于卫星，其坐标系原点在卫星本体质心处（求解姿态相关时，与原点无关），VVLH三个坐标轴的定义如下（前右下坐标系）：
X: 沿飞行方向，由Y×Z确定；
Y: 轨道面负法向；
Z: 指向地心方向；
需要注意，对于卫星，其轨道是定义在地心惯性系下的（地固系和地心惯性系下的卫星轨道面法向有所不同）。
X轴的定义沿飞行方向，不一定与卫星的飞行速度矢量重合，而是由Y轴和Z轴叉乘决定。只有当卫星的轨道为圆轨道时，X轴才与飞行速度矢量重合。

**方位角、高度角**
STK中，定义一个矢量的方位角和高度角通常在VVLH坐标系下定义的。如太阳矢量的方位角和高度角。
方位角，英文名Azimuth,简称Az。定义为矢量在XY平面内投影与X轴的夹角，向Y轴方向为正。
高度角，英文名Elevation,简称El。定义为矢量与XY平面的夹角，向-Z轴方向为正。

[STK中的VVLH坐标系及方位角、高度角](https://blog.csdn.net/u011575168/article/details/116991086?spm=1001.2014.3001.5502)

## 3 传感器
为卫星添加传感器（Sensor）,设定圆锥半角为44.85°

![](https://img-1258201770.cos.ap-beijing.myqcloud.com/imgs/202209192052781.png)

## 4 地面站(facility)
### 4.1 插入地面站数据库
[[30-论文/软件/STK使用#^40t436]]

## 5 参考文献
[知乎-小脏鱼儿](https://www.zhihu.com/people/xiao-zang-yu-59/posts): python与stk联合仿真, 详细教程

[知乎-戴正旭](https://zhuanlan.zhihu.com/p/68385977): 基于STK/Matlab的Starlink星座仿真分析, 里面有许多starlink的相关资料

[csdn-wangyulj](https://blog.csdn.net/wangyulj/article/details/123664133): STK9中自建数据库批量插入地面设施（Facility） ^40t436

[知乎-STK Satellite全属性配置教程（图文）](https://zhuanlan.zhihu.com/p/554947207)





