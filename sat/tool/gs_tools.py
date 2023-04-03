from datetime import datetime
from sat.tool.file_tools import get_yaml

from sat.obj.gs import GroundStation
def auto_get_gs_list(sat_dict, filename='../conf.yaml'):
    print(f"{datetime.now().isoformat()}    开始生成地面站")

    result = get_yaml(filename)
    str_list = result['gs']

    gs_list = []
    for str in str_list:
        gs_items = str.split(' ')
        name = gs_items[0] + ' ' + gs_items[1]
        lat = float(gs_items[2])
        lon = float(gs_items[3])
        height = float(gs_items[4])
        degree = float(gs_items[5])
        gs = GroundStation(name, lat, lon, height, degree, sat_dict)
        gs_list.append(gs)

    return gs_list
