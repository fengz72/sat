# cesium
## 1 入门
### 1.1 导入
使用npm安装, `npm install cesium`
在项目里导入
```html
<script src="../node_modules/cesium/Build/Cesium/Cesium.js"></script>
<style>
    @import url(../node_modules/cesium/Build/Cesium/Widgets/widgets.css);
    html,
    body,
    #cesiumContainer {
        width: 100%;
        height: 100%;
        margin: 0;
        padding: 0;
        overflow: hidden;
    }
</style>
```

或者使用cdn导入
```html
<script src="https://cesium.com/downloads/cesiumjs/releases/1.103/Build/Cesium/Cesium.js"></script> 
<link href="https://cesium.com/downloads/cesiumjs/releases/1.103/Build/Cesium/Widgets/widgets.css" rel="stylesheet">
```

### 1.2 hello
在body中创建控件
```html
<div id='cesiumContainer'></div>
```

使用脚本控制:
- 直接
  ```html
  <script>
	    Cesium.Ion.defaultAccessToken = ''
	    const viewer = new Cesium.Viewer('cesiumContainer', {
	        terrainProvider: Cesium.createWorldTerrain()
	    }); 
    </script>
	```
- 创建一个js文件

### 1.3 token
[cesium-access tokens](https://ion.cesium.com/tokens?page=1)

## 2 界面
### 2.1 界面元素
![image.png](https://img-1258201770.cos.ap-beijing.myqcloud.com/imgs/202303151717972.webp)

![image.png](https://img-1258201770.cos.ap-beijing.myqcloud.com/imgs/202303151718801.webp)

使用js控制
```js
const viewer = new Cesium.Viewer('cesiumContainer', {
  baseLayerPicker: false,  // 影像切换
  animation: true,  //是否显示动画控件
  infoBox: false, //是否显示点击要素之后显示的信息
  geocoder: false, //是否显示地名查找控件
  timeline: true, //是否显示时间线控件
  fullscreenButton: false,
  shouldAnimate: false,
  navigationHelpButton: false, //是否显示帮助信息控件
  terrainProvider: new Cesium.createWorldTerrain({
    requestWaterMask: true, //是否请求额外的水数据
    requestVertexNormals: true // 光数据
  }), //地形, createWorldTerrain由官方提供
  imageryProvider: new Cesium.UrlTemplateImageryProvider({
	url: "http://mt1.google.cn/vt/lyrs=s&hl=zh-CN&x={x}&y={y}&z={z}&s=Gali"
  })
});
```


## 3 czml
>CZML是一种用来描述动态场景的JSON架构的语言，主要用于Cesium在浏览器中的展示。它可以用来描述点、线、布告板、模型以及其他的图元，同时定义他们是怎样随时间变化的。Cesium拥有一套富客户端API，通过CZML采用数据驱动的方式，不用写代码我就可以使用通用的Cesium viewer构建出丰富的场景。

我们将CZML标准以及它的相应实现分为4个部分：
- CZML Structure --  CZML文档的整体结构
- CZML Content --内容
- CZML in Cesium -- Cesium中解析和显示CZML的流程
- czml-writer-Architecture –czml-writer的架构

### 3.1 入门
一个有效的CZML文档同时也是一个有效的JSON文档, 一个CZML文档包含一个JSON数组，数组中个每一个对象都是一个CZML数据包（packet），一个packet对应一个场景中的对象，例如一个飞机。

需要以`id`为`document`的packet开头
```json
{  
    "id": "document",  
    "name": "CZML Point - Time Dynamic",  
    "version": "1.0",  
    "clock": {  
        "interval": '2022-01-01T10:10:10+0800/2022-01-05T10:10:10+0800', '2022-01-06T10:10:10+0800/2022-01-08T10:10:10+0800'
        "multiplier": 1,  
        "range": "LOOP_STOP",  
        "step": "SYSTEM_CLOCK"  
    }  
}
```

时间间隔**interval**为一个数组, 每一个元素代表开始到结束的时间段. 遵循ISO8601格式.

具体属性参考:
- [csdn-Cesium Language (CZML) 入门1 — CZML Structure（CZML的结构）](https://www.cnblogs.com/laixiangran/p/4997971.html)
- [csdn-Cesium Language (CZML) 入门2 — CZML Content（CZML的内容）](https://www.cnblogs.com/laixiangran/p/4998529.html)
- [gthub-CZML文件官方文档](https://github.com/AnalyticalGraphicsInc/czml-writer/wiki)

### 3.2 卫星轨迹
```json
{  
    "id": "Satellite/ppCOSMOS 2426 (717)",  // id, 需要唯一, 可以通过id引用其他packet
    "name": "1_1",  
    "availability": "2022-03-22T16:08:00+08:00/2022-03-23T16:08:00+08:00",  
    "label": {  // 标签
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
        "show": True,  
        "style": "FILL_AND_OUTLINE",  
        "text": f'{sat.name}',  
        "verticalOrigin": "CENTER"  
    },  
    "path": {  // 路径, 比较关键的是leadTime和trailTime属性
        "show": [  
            {  
                "interval": f'{initialTime}/{endTime}',  
                "boolean": True  
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
    // "model": {  
    //     "show": True,    
    //     "gltf": "./111.gltf",    
    //     "minimumPixelSize": 50,    
    // },    
    "position": {  
        "interpolationAlgorithm": "LAGRANGE",  
        "interpolationDegree": 5,  
        // 参考坐标系，地惯坐标系  
        "referenceFrame": "INERTIAL",  
        "epoch": "2022-03-22T16:08:00+08:00",  
        "cartesian": [
              0,
              10246472.183615023,
              23315473.78200593,
              -99942.77560130549,
              300,
              9768930.236227807,
              23491323.358455077,
              -1173388.669547688,
              ]
    }  
}
```

`position`中的属性:
- `referenceFrame`: 参考系框架
	- `FIXED`: 地固系(ECEF), WGS84和ITRF属于地固系
	- `INERTIAL`: 惯性系(ECI)
- `cartesian`: 数组, 格式为`[time,x,y,z,time,x,y,z,...]`, 其中时间为epoch以来的秒数
- `cartographicDegrees\cartographicRadians`: 数组, 格式为`[time,lon,lat,height,time,lon,lat,height,...]`, 以WGS84为参考系
  此属性与`cartesian`选择一个就行, 选择此属性是, `referenceFrame`应为`FIXED`. 此属性分为角度和弧度.

## 4 参考链接
- [cesium官网](https://cesium.com/)
- [gthub-CZML文件官方文档](https://github.com/AnalyticalGraphicsInc/czml-writer/wiki)
- [cesium中文网](http://cesium.xin/wordpress/): 里面有一些教程和中文api
- [cesium中文网](http://cesiumcn.org/): 论坛
- [博客园-laixiangran:Cesium](https://www.cnblogs.com/laixiangran/tag/Cesium/): 一些关于Cesium的文章
- [csdn-Cesium实现卫星在轨绕行](https://blog.csdn.net/weixin_42776111/article/details/125479398): 使用js画出卫星和轨道
- [csdn-Cesium学习之CZML的使用](https://blog.csdn.net/Gua_guagua/article/details/125024376?spm=1001.2014.3001.5501): czml文件的构成
- [csdn-使用TLE轨道两行数计算轨道信息，并生成CZML格式文件](https://blog.csdn.net/Gua_guagua/article/details/126895330?spm=1001.2014.3001.5501): 使用js生成卫星的czml文件

