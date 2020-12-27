# 计算机软件基础大作业

## 版权说明

CopyRight ( 2020- ) : YangHui, Kamarov  @BUAA

## 服务端说明

服务端通过serverCore copy.py启动，启动要求在同文件目录下有groupInfo.json和userInfo.json文件，文件内部都写入一个“[]”表示一个空列表。

服务端的服务器ip默认使用127.0.0.1hostIP地址，端口号1919，请检查是否有冲突占用

## 客户端说明

客户端启动需要安装pyqt5, pyaudio库，其中pyaudio库可能无法使用pip下载，请从如下网址下载pyaudio库并安装使用。[pyaudio库下载地址](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)

下载完毕以后直接使用示例代码安装包即可，注意版本号

~~~cmd
pip install C:\Users\UserName\Downloads\PyAudio-0.2.11-cp39-cp39-win_amd64
~~~

客户端启动代码为Client文件夹下的Client.py文件，客户端启动时服务端必须先开启

客户端不同设备之间音频传输使用8086端口，请检查是否有冲突；客户端在本机音频传输使用8086、8087端口。不同设备之间的文件传输使用8088端口；客户端在本机传输文件使用8088、8089端口。在启动的时候请手动修改clientCore的初始化数值

~~~python
audioPort = 8087
audioConnectPort = 8086
filePort = 8088
fileConnectPort = 8089

audioPort = 8086
audioConnectPort = 8087
filePort = 8089
fileConnectPort = 8088
~~~

这两个在同一台设备上启动两个不同客户端的时候要进行更换。

## 可能存在的问题

由于开发时间紧张，难免会有错误，恳请各位斧正。以下是可能存在的错误。

1. 文件发送过程中中断有可能导致对方数据错误，甚至有可能导致对方数据无法重新接收文件；

2. 客户端退出的时候服务端可能会有标志位清理不干净的情况，需要反复的测试得到结果。

## 版本说明

Version:

* 本项目暂时以2.3.0作为最终发布版本

2.3.0 release 各项工作收尾完毕，细节处理完成

2.2.0 release 文件传输完善完毕

2.2.0 beta 加入了文件传输

2.1.1 release 取消了文件发送的双方确认机制

2.1.0 release 解决了语音聊天机制中的退出bug，GUI界面的人性化方面进行改良

2.1.0 beta 添加了语音聊天机制，存在退出bug需要解决

2.0.1 release 解决了GUI界面的异常退出bug，添加了服务器重启断点复原功能

2.0.1 beta 完全开发了GUI界面

2.0.0 beta GUI界面开始测试前后端连接

* 1.x.x所有版本都为核心内部测试版本，没有公布版本

1.2.0 beta 群组管理系统上线

1.1.0 beta 初步建立了以群组作为基本聊天单元的线程管理机制

1.0.0 beta 开发了基本的消息互传和登录系统

## 鸣谢

感谢@Kamarov对本项目的支持。其本人尚未注册GitHub账号，若有注册立刻更新链接。

感谢和合作的[@Narukara](https://github.com/Narukara)的SmartPlug服务器参考支持。

欢迎访问我的小破站[YangHui的小站——“阳之所至，万象朝辉”](https://ling-yanghui.github.io/)