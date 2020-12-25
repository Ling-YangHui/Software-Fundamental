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

## 版本说明

Version:

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