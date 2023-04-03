import yaml
import os


def get_yaml(filename):
    """
    得到配置文件
    :param filename: 配置文件路径
    :return: 字典
    """
    if not os.path.exists(filename):
        print(filename + ' 文件不存在...')
        exit(1)

    with open(filename, 'r', encoding='utf-8') as f:
        result = yaml.load(f.read(), Loader=yaml.FullLoader)

    return result


