## 1 安装

### 1.1 命令
```bash
sudo apt install g++ python3

sudo apt install g++ python3 python3-dev pkg-config sqlite3

sudo apt install python3-setuptools git

sudo apt install qt5-default mercurial 
sudo apt install gir1.2-goocanvas-2.0 python-gi python-gi-cairo python-pygraphviz python3-gi python3-gi-cairo python3-pygraphviz gir1.2-gtk-3.0 ipython ipython3

sudo apt install openmpi-bin openmpi-common openmpi-doc libopenmpi-dev

sudo apt install autoconf cvs bzr unrar

sudo apt install gdb valgrind

sudo apt install uncrustify

sudo apt install doxygen graphviz imagemagick
sudo apt install texlive texlive-extra-utils texlive-latex-extra texlive-font-utils dvipng latexmk

sudo apt install python3-sphinx dia

sudo apt install gsl-bin libgsl-dev libgslcblas0

sudo apt install tcpdump

sudo apt install sqlite sqlite3 libsqlite3-dev

sudo apt install libxml2 libxml2-dev

sudo apt install cmake libc6-dev libc6-dev-i386 libclang-dev llvm-dev automake python3-pip
python3 -m pip install --user cxxfilt

sudo apt install libgtk-3-dev

sudo apt install vtun lxc uml-utilities

sudo apt install libxml2 libxml2-dev libboost-all-dev

```

```bash
cd ~
git clone https://gitlab.com/nsnam/bake -- 从gitlab克隆项目 export BAKE_HOME=`pwd`/bake -- 将bake的路径加入系统路径 
export PATH=$PATH:$BAKE_HOME 
export PYTHONPATH=$PYTHONPATH:$BAKE_HOME 
cd /bake # 进入bake文件夹 
./bake.py check # 检查依赖是否已经安装完成

```

```bash

./bake.py configure -e ns-3.30 # 指定下载NS3的版本号
./bake.py show   
./bake.py download -vvv #下载
./bake.py build -vvv #build

```

```bash
cd ./source/ns3.35
./waf configure --enable-examples --enable-tests
-- 出现以下则成功
-- Python API Scanning Support : enabled 
-- Python Bindings : enabled

./test.py
-- 全PASS

```

运行.py文件
```bash
./waf shell #推荐
python3 examples/tutorial/first.py

./waf --pyrun example/tutorial/first.py

```
### 1.2 参考链接
- [知乎 - 妈妈咪呀](https://www.zhihu.com/people/zhang-shi-qi-89-26/posts)
- [官网-安装](https://www.nsnam.org/wiki/Installation#Installation)
- [官网-下载](https://www.nsnam.org/releases/ns-3-35/)
- [PyBindGen](https://pypi.org/project/PyBindGen/0.22.0/)
- [csdn-Rookie](https://www.cnblogs.com/huang-xiang/p/13967012.html)

### 1.3 issue
- `Building pybindgen-0.22.0 - Problem`
  ```bash
  pip install PyBindGen==0.22.0
	```

- pygccxml
  ```bash
  pip install pygccxml
	```

- castXML
  ```bash
  pip3 install CastXML -- 之后一定要重启
	```


## 2 学习

### 2.1 基本概念
- 节点(Node)
  用于描述各种主机的抽象, 由C++编写的Node类描述
- 信道
  由Channel类描述
- 网络设备
  总是安装在节点上, 相当于硬件设备和驱动软件的总和. 由NetDevice类描述, NetDevice类提供了管理连接其他节点和信道对象的各种方法
- 应用程序
  需要被仿真的用户程序被抽象为应用。用Application类来描述, 这个类提供了管理仿真过程中用户层应用的各种方法

### 2.2 创建.cc文件并运行

```bash
cp examples/tutorial/first.cc scratch/myfirst.cc
./waf  # 会编译
./waf --run scratch/myfirst  -- 运行

```
编译后的文件会被放到`build/scratch/`目录下

### 2.3 开始停止
```cpp
Simulator::Stop(Seconds(11.0));  
Simulator::Run();  
Simulator::Destroy();  
return 0;
```

### 2.4 日志
[日志](https://blog.51cto.com/u_847102/5269522)

**开始**
```c++
NS_LOG_COMPONENT_DEFINE ("FirstScriptExample");
```
使用宏定义一个日志模块
**日志级别**
- NS_LOG_ERROR — 记录错误信息;
- NS_LOG_WARN — 记录警告信息;
- NS_LOG_DEBUG — 记录相对不常见的调试信息;
- NS_LOG_INFO — 记录程序进展信息;
- NS_LOG_FUNCTION — 记录描述每个调用函数信息;
- NS_LOG_LOGIC – 记录一个函数内描述逻辑流程的信息;
- NS_LOG_ALL — 记录所有信息.
- NS_LOG_UNCOND — 无条件输出

```bash
LogComponentEnable("UdpEchoClientApplication", LOG_LEVEL_INFO);
# 在shell上输出日志
export NS_LOG=UdpEchoClientApplication=level_all
# 显示产生此条日志的组件名
export 'NS_LOG=UdpEchoClientApplication=level_all|prefix_func'

# 用:隔开不同的组件名
export 'NS_LOG=UdpEchoClientApplication=level_all|prefix_func:UdpEchoServerApplication=level_all|prefix_func'

# 通配符*, 显示所有组件
export 'NS_LOG=*=level_all|prefix_func|prefix_time'

# 将所有日志输出到文件
./waf --run scratch/myfirst > log.out 2>&1
```

[[20-code/Tools/linux/linux#^1e3698]]

**清除日志级别**
```bash
export NS_LOG=
```

**自定义日志**
```c++
// 在源码需要加上日志的地方
NS_LOG_INFO ("Creating Topology");

export NS_LOG=FirstScriptExample=info

```

**使用命令行来为程序提供参数**
```c++
CommandLine cmd (__FILE__);  
cmd.Parse (argc, argv);
```

```bash
./waf --run "scratch/myfirst --PrintHelp"
```
![](https://img-1258201770.cos.ap-beijing.myqcloud.com/imgs/202209291536520.png)

```bash
# 打印PointToPointNetDevice的所有属性
./waf --run "scratch/myfirst --PrintAttributes=ns3::PointToPointNetDevice"
```

```bash
# 使用命令行来提供参数
./waf --run "scratch/myfirst

    --ns3::PointToPointNetDevice::DataRate=5Mbps

    --ns3::PointToPointChannel::Delay=2ms

    --ns3::UdpEchoClient::MaxPackets=2"
```

**自定义钩子**
```c++
uint32_t nPackets = 1;  
  
CommandLine cmd (__FILE__);  
cmd.AddValue("nPackets", "Number of packets to echo", nPackets);  
cmd.Parse (argc, argv);
...
echoClient.SetAttribute ("MaxPackets", UintegerValue (nPackets));
```
```bash
./waf
./waf --run "scratch/myfirst --PrintHelp"
./waf --run "scratch/myfirst --nPackets=2"
```

**Tracing**
```c++
tcpdump -nn -tt -r myfirst-0-0.pcap
```
[[res/ns-3-tutorial.pdf]], 6.3Using the Tracing System

### 2.5 temp
```bash
tcpdump -nn -tt -r second-0-0.pcap
```

### 2.6 资料
- [csdn-卫星网络相关网址](https://blog.csdn.net/bajiaoyu517/article/details/116231457)

### 2.7 参考链接
- [官方api文档](https://www.nsnam.org/docs/release/3.36/doxygen/_type_id_list.html)
- [中文文档-入门](https://blog.51cto.com/u_847102/5269538)
- [中文文档-Tweaking](https://blog.51cto.com/u_847102/5269530)
- [中文文档-主页](https://blog.51cto.com/search/user?uid=837102&q=ns3%E7%B3%BB%E5%88%97)
- [ns3-卫星模型](https://gitlab.inesctec.pt/pmms/ns3-satellite)