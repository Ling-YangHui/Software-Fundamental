# 计算机软件基础大作业

## 版权说明

CopyRight ( 2020- ) : YangHui, Kamarov  @BUAA

## 服务端说明

服务端通过serverCore copy.py启动，启动要求在同文件目录下有groupInfo.json和userInfo.json文件，文件内部都写入一个“[]”表示一个空列表。

服务端的服务器ip默认使用127.0.0.1hostIP地址，端口号1919，请检查是否有冲突占用

## 客户端说明

客户端启动需要安装pyqt5库

客户端启动代码为Client文件夹下的Client.py文件，客户端启动时服务端必须先开启

客户端不同设备之间音频传输使用8086端口，请检查是否有冲突；客户端在本机音频传输使用8086、8087端口，在启动的时候请手动修改clientCore的初始化数值

~~~python
audioPort = 8086
connectPort = 8087
~~~

这两个在同一台设备上启动两个不同客户端的时候要进行更换。