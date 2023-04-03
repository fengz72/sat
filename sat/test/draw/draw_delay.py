import matplotlib.pyplot as plt
import os, time, math

def draw():
    length = 7
    dir_path = '../beijing China to Hainan China'


    for r, d, f in os.walk(dir_path):
        for file in f:
            if '.txt' in file:
                count = 0
                times = []
                nums = []
                dis = []
                delay = []
                with open(dir_path + '/' + file, 'r', encoding='utf-8') as f:
                    result = f.readlines()
                    for i in range(0, len(result)):
                        if i % length == 0:
                            t = time.strptime(result[i][6:25], '%Y-%m-%d %H:%M:%S')
                            times.append(t)
                        if i % length == 3:
                            n = int(result[i].split(': ')[1])
                            nums.append(n)
                        if i % length == 4:
                            d = float(result[i].split(' ')[1])
                            dis.append(d)
                        if i % length == 5:
                            de = float(result[i].split(' ')[1])
                            delay.append(de)

                x = range(0, len(times))

                plt.title(file.split('.')[0])
                plt.plot(x, delay)
                plt.ylabel('delay / ms')
                plt.show()

                plt.title(file.split('.')[0])
                plt.plot(x, nums)
                plt.ylabel('num')
                plt.show()

                plt.title(file.split('.')[0])
                plt.plot(x, dis)
                plt.ylabel('distance / km')
                plt.show()

def draw_tset():
    length = 7
    dir_path = '/mnt/d/workSpace/exp/satellite-topology/data/delay/2023-03-13_12-29-07'


    for r, d, f in os.walk(dir_path):
        row = 1
        col = 3
        for file in f:
            count = 0
            times = []
            nums = []
            dis = []
            delay = []
            with open(dir_path + '/' + file, 'r', encoding='utf-8') as f:
                result = f.readlines()
                for i in range(0, len(result)):
                    if i % length == 0:
                        t = time.strptime(result[i][6:25], '%Y-%m-%d %H:%M:%S')
                        times.append(t)
                    if i % length == 3:
                        n = int(result[i].split(': ')[1])
                        nums.append(n)
                    if i % length == 4:
                        d = float(result[i].split(' ')[1])
                        dis.append(d)
                    if i % length == 5:
                        de = float(result[i].split(' ')[1])
                        delay.append(de)

            x = range(0, 59)
            count += 1
            plt.subplot(row, col, count)
            plt.plot(x, delay)
            plt.ylabel('delay / ms')

            count += 1
            plt.subplot(row, col, count)
            plt.plot(x, nums)
            plt.ylabel('num')

            count += 1
            plt.subplot(row, col, count)
            plt.plot(x, dis)
            plt.ylabel('distance / km')
            plt.show()


def test():
    x = [1, 2, 3]
    y1 = [2, 4, 1]
    y2 = [4000, 3000, 2000]

    fig, ax1 = plt.subplots()

    ax1.plot(x, y1)
    ax1.set_xlabel('X Axis Label')
    ax1.set_ylabel('Y Axis Label for y1')

    ax2 = ax1.twinx()
    ax2.plot(x, y2)
    ax2.set_ylabel('Y Axis Label for y2')

    plt.title('My Plot Title')
    plt.show()

if __name__ == '__main__':
    # test()
    # draw_tset()
    draw()

