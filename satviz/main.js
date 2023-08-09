// import * as Cesium from "cesium"

Cesium.Ion.defaultAccessToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI3ZDdjNTY2Ni1kOWZjLTRhMDQtOGY5ZC1mNzg3OGZjNzJkZjciLCJpZCI6MTI3NjMzLCJpYXQiOjE2NzgxNzg5MjV9._gYYf-wEPs2NlwuOMQwh8k37Z3FGqqr2TSMOaZDLrE8';

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
        requestWaterMask: true,
        requestVertexNormals: true
    }),
    // imageryProvider: new Cesium.UrlTemplateImageryProvider({
    //     url: "http://mt1.google.cn/vt/lyrs=s&hl=zh-CN&x={x}&y={y}&z={z}&s=Gali"
    // })
});

let isoStart = '2023-03-01T01:01:09Z';
let lat = [50, 30, 20];
let lon = [50, 30, 20];
let height = [550 * 1000, 550 * 1000, 24.5];



function getData() {
    // fetch('http://127.0.0.1:5500/data/beijing China to London UK/2023-03-01 00-00-57.json')
    // fetch('http://127.0.0.1:5500/data/beijing China to London UK/2023-03-01 00-00-58.json')
    fetch('http://127.0.0.1:55001/data/beijing China to Hainan China/2023-03-01 00-00-57.json')
    // fetch('http://127.0.0.1:5500/data/beijing China to Hainan China/2023-03-01 00-00-58.json')
        .then(function (response) {
            if (response.ok) {
                return response.text();
            }
            throw new Error('请求失败');
        }).then(function (data) {
            console.log("返回的数据", data);
            let obj = JSON.parse(data); // 转为对象
            //设置时间
            let isoStart = obj.time;
            setTime(isoStart);

            let path = obj.path;

            let satList = obj.sat;
            let gsList = obj.gs;
            console.log(satList[0].pos, gsList);
            addEntites(satList, gsList, path);

            let links = obj.link;
            addlink(links, satList, gsList, path);

            addPath(satList, gsList, path);
        }).catch(function (error) {
            console.log(error);
        })
}

function setTime(isoStart) {
    let start = new Cesium.JulianDate.fromIso8601(isoStart);
    viewer.clock.startTime = start.clone();
}

function addEntites(satList, gsList, path) {
    // for (let i = 0; i < satList.length; i++) {
    //     if (true) {
    //         let sat = satList[i];
    //         let temp = viewer.entities.add({
    //             name: sat.name,
    //             position: Cesium.Cartesian3.fromArray(sat.pos),
    //             ellipsoid: {
    //                 radii: new Cesium.Cartesian3(67500.0, 67500.0, 67500.0),
    //                 material: Cesium.Color.BLUE
    //             }
    //         });
    //         // temp.label = {
    //         //     text: sat.name,
    //         //     font: '18px Helvetica',
    //         //     fillColor: Cesium.Color.WHITE,
    //         //     outlineColor: Cesium.Color.BLACK,
    //         //     outlineWidth: 2,
    //         //     style: Cesium.LabelStyle.FILL_AND_OUTLINE,
    //         //     horizontalOrigin: Cesium.HorizontalOrigin.CENTER,
    //         //     verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
    //         //     pixelOffset: new Cesium.Cartesian2(0, -10)
    //         // };
    //     }
    // }
    satList.forEach(sat => {
        let color = Cesium.Color.BLUE;
        if (true) {
            path.forEach(p => {
                if (sat.name == p) {
                    color = Cesium.Color.RED;
                }
            });
            let temp = viewer.entities.add({
                name: sat.name,
                position: Cesium.Cartesian3.fromArray(sat.pos),
                ellipsoid: {
                    radii: new Cesium.Cartesian3(67500.0, 67500.0, 67500.0),
                    material: color
                }
            });
            // temp.label = {
            //     text: sat.name,
            //     font: '18px Helvetica',
            //     fillColor: Cesium.Color.WHITE,
            //     outlineColor: Cesium.Color.BLACK,
            //     outlineWidth: 2,
            //     style: Cesium.LabelStyle.FILL_AND_OUTLINE,
            //     horizontalOrigin: Cesium.HorizontalOrigin.CENTER,
            //     verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
            //     pixelOffset: new Cesium.Cartesian2(0, -10)
            // };
        }
    })

    gsList.forEach(gs => {
        let color = Cesium.Color.GREEN;
        path.forEach(p => {
            if (gs.name == p) {
                color = Cesium.Color.RED;
            }
        });
        let temp = viewer.entities.add({
            name: gs.name,
            position: Cesium.Cartesian3.fromArray(gs.pos),
            ellipsoid: {
                radii: new Cesium.Cartesian3(67500.0, 67500.0, 67500.0),
                material: color
            }
        });
        // temp.label = {
        //     text: gs.name,
        //     font: '18px Helvetica',
        //     fillColor: Cesium.Color.WHITE,
        //     outlineColor: Cesium.Color.BLACK,
        //     outlineWidth: 2,
        //     style: Cesium.LabelStyle.FILL_AND_OUTLINE,
        //     horizontalOrigin: Cesium.HorizontalOrigin.CENTER,
        //     verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
        //     pixelOffset: new Cesium.Cartesian2(0, -10)
        // };
    });
}

function addlink(links, satList, gsList, path) {
    let satPos1 = [];
    let satPos2 = [];

    links.forEach(link => {
        satList.forEach(sat => {
            if (sat.name == link[0]) {
                satPos1 = sat.pos;
            }
            if (sat.name == link[1]) {
                satPos2 = sat.pos;
            }
        });
        gsList.forEach(gs => {
            if (gs.name == link[1]) {
                satPos2 = gs.pos;
            }
        });
        viewer.entities.add({
            polyline: {
                positions: [Cesium.Cartesian3.fromArray(satPos1), Cesium.Cartesian3.fromArray(satPos2)],
                width: 1,
                material: Cesium.Color.WHITE
            }
        });


    });
}

function addPath(satList, gsList, path) {
    // let pos1 = [];
    // let pos2 = [];
    let gsName = "";
    let satName = "";
    for (let i = 0; i < path.length - 1; i++) {
        let posList = [];
        if (i == 0 || i == path.length - 2) {
            if (i == 0) {
                gsName = path[i];
                satName = path[i+1];
            }else{
                gsName = path[i+1];
                satName = path[i];
            }
            satList.forEach(sat => {
                if (sat.name == satName) {
                    // pos1 = sat.pos;
                    posList.push(sat.pos);
                }
            });
            gsList.forEach(gs => {
                if (gs.name == gsName) {
                    // pos2 = gs.pos;
                    posList.push(gs.pos);
                }
            });
        }else {
            satList.forEach(sat => {
                if (sat.name == path[i] || sat.name == path[i+1]) {
                    posList.push(sat.pos);
                }
            });
        };
        console.log(posList);
        viewer.entities.add({
            polyline: {
                positions: [Cesium.Cartesian3.fromArray(posList[0]), Cesium.Cartesian3.fromArray(posList[1])],
                width: 1,
                material: Cesium.Color.RED
            }
        });
    }
}

function setSatPosition() {
    let sat_entity0 = viewer.entities.add({
        name: "1_1",
        position: Cesium.Cartesian3.fromDegrees(lat[0], lon[0], height[0]),
        ellipsoid: {
            radii: new Cesium.Cartesian3(67500.0, 67500.0, 67500.0),
            outline: true,
            outlineColor: Cesium.Color.WHITE,
            outlineWidth: 2,
            material: Cesium.Color.BLUE
        }
    });
    sat_entity0.label = {
        text: sat_entity0.name,
        font: '18px Helvetica',
        fillColor: Cesium.Color.WHITE,
        outlineColor: Cesium.Color.BLACK,
        outlineWidth: 2,
        style: Cesium.LabelStyle.FILL_AND_OUTLINE,
        horizontalOrigin: Cesium.HorizontalOrigin.CENTER,
        verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
        pixelOffset: new Cesium.Cartesian2(0, -10)
    };

    let sat_entity1 = viewer.entities.add({
        position: Cesium.Cartesian3.fromDegrees(lat[1], lon[1], height[1]),
        ellipsoid: {
            radii: new Cesium.Cartesian3(67500.0, 67500.0, 67500.0),
            outline: true,
            outlineColor: Cesium.Color.WHITE,
            outlineWidth: 2,
            material: Cesium.Color.BLUE
        }
    });

    setLinkLine(sat_entity0, sat_entity1);
}

function setLinkLine(sat_entity0, sat_entity1) {
    console.log(typeof (sat_entity0.position.getValue()), sat_entity1.position.getValue());
    let line = viewer.entities.add({
        polyline: {
            positions: [sat_entity0.position.getValue(), sat_entity1.position.getValue()],
            width: 1,
            material: Cesium.Color.WHITE
        }
    });
}

function sat() {
    // setSatPosition();
    // setTime();
    getData();
}

sat()
