import os
import arrow
from datetime import datetime

from shortest import calc_all

from sat.tool.satviz_tools import auto_czml

def main():
    # 得到文件保存路径
    time_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    dir_path = f'../data/{time_str}/'
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    print(f'{arrow.now().isoformat()}  文件保存路径为{dir_path}')

    # 计算最短路径
    calc_all(dir_path, '../test.yaml')
    # 可视化
    for dirpath, dirnames, filenames in os.walk(dir_path):
        for filename in filenames:
            if filename.endswith('.json'):
                auto_czml(dir_path, dir_path, filename, save_filename=f"{filename.replace('.json', '.czml')}", conf_path='../test.yaml')

if __name__ == '__main__':
    main()